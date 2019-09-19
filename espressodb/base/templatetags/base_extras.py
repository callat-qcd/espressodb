"""Additional in template functions for the espressodb module
"""
from django import template

from django_extensions.management.commands.show_urls import Command as URLFinder

from espressodb.management.utilities.settings import PROJECT_APPS
from espressodb.management.utilities.version import get_repo_version
from espressodb.management.utilities.version import get_db_info
from espressodb.base.utilities.apps import get_apps_slug_map
from espressodb.base.utilities.apps import get_app_name
from espressodb.base.urls import urlpatterns
from espressodb.base.forms import MODELS

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list(
    exclude=("", "populate", "populate-result", "admin", "documentation")
):
    """Renders all links as a nested list
    """
    u = URLFinder()
    view_infos = u.extract_views_from_urlpatterns(urlpatterns)

    urls = {}
    for view, path, reverse_name in view_infos:

        if path.split("/")[0] in exclude:
            continue

        import_path = view.__module__.split(".")

        if import_path[0] != "espressodb":
            continue

        app_name = import_path[1].capitalize()
        link_name = reverse_name.split(":")[-1].capitalize()

        if app_name in urls:
            urls[app_name].append((link_name, reverse_name))
        else:
            urls[app_name] = [(link_name, reverse_name)]

    documentation = []
    if "espressodb.documentation" in PROJECT_APPS:
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


@register.simple_tag
def render_version() -> str:
    """Returns descriptive version string
    """
    branch, version = get_repo_version()
    branch = f" ({branch})" if branch else ""
    return version + branch if version else ""


@register.simple_tag
def render_db_info() -> str:
    """Returns descriptive db string
    """
    name, user = get_db_info()
    return f"{user}@{name}"
