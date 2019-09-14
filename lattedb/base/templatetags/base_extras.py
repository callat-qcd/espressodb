"""Additional in template functions for the lattedb module
"""
from django import template

from django_extensions.management.commands.show_urls import Command as URLFinder

from lattedb.config.urls import urlpatterns
from lattedb.config.settings import PROJECT_APPS

from lattedb.base.utilities.models import get_apps_slug_map, get_app_name
from lattedb.base.forms import MODELS

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list(exclude=("", "base", "admin", "documentation")):
    """Renders all links as a nested list
    """
    u = URLFinder()
    view_infos = u.extract_views_from_urlpatterns(urlpatterns)

    urls = {}
    for view, path, reverse_name in view_infos:

        if path.split("/")[0] in exclude:
            continue

        import_path = view.__module__.split(".")

        if import_path[0] != "lattedb":
            continue

        app_name = import_path[1].capitalize()
        link_name = reverse_name.split(":")[-1].capitalize()

        if app_name in urls:
            urls[app_name].append((link_name, reverse_name))
        else:
            urls[app_name] = [(link_name, reverse_name)]

    if "lattedb.documentation" in PROJECT_APPS:
        documentation = []
        for app_slug, app in get_apps_slug_map().items():
            documentation.append((app_slug, get_app_name(app)))

    context = {"urls": urls, "documentation": documentation}

    return context


@register.inclusion_tag("tree-to-python.html")
def render_tree(tree, root):
    content = ""
    models = {}

    labels = set(tree.values())
    labels.add(root)

    for label in labels:
        model = MODELS[label]
        module = model.__module__
        cls = model.__name__
        app = model._meta.app_label  # pylint: disable=W0212
        name = cls + app.capitalize()
        content += f"from {module} import {cls} as {name}\n"
        models[label] = (name, model)

    content += "\n"

    for name, label in list(tree.items())[::-1]:
        cls, model = models[label]
        fields = model.get_open_fields()
        args = "\n\t".join(
            [f"{field.name}=..., # {field.help_text}" for field in fields]
        )
        name = name.replace(".", "_")
        content += f"{name} = {cls}.get_or_create(\n\t{args}\n)\n\n"

    cls, model = models[root]
    fields = model.get_open_fields()
    args = "\n\t".join([f"{field.name}=..., # {field.help_text}" for field in fields])
    name = name.replace(".", "_")
    content += f"{cls}.get_or_create(\n\t{args}\n)"

    context = {"content": content}
    return context
