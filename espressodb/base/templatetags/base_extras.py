"""Additional in template functions for the base module.
"""
from typing import List, Dict, Tuple

from django import template
from django.conf import settings
from django.db.models.fields import Field
from django.template.defaultfilters import Truncator

from django.urls import reverse, NoReverseMatch

from django_extensions.management.commands.show_urls import Command as URLFinder

from espressodb.management.utilities.settings import PROJECT_NAME
from espressodb.management.utilities.version import get_repo_version
from espressodb.management.utilities.version import get_db_info
from espressodb.base.utilities.apps import get_apps_slug_map
from espressodb.base.utilities.apps import get_app_name
from espressodb.base.forms import MODELS


register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list(
    exclude=("", "populate", "populate-result", "admin", "documentation")
) -> Dict[str, Tuple[str, str]]:
    """Renders all app and documentation page links

    Arguments:
        exclude: The link names to exclude.

    Returns:
        Context with keys ``urls`` and ``documentation`` where each value is a list
        of Tuples with the reverse url name and display name.

    Ignores urls which do not result in a match.

    Uses the template ``link-list.html``.
    """
    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])

    u = URLFinder()
    view_infos = u.extract_views_from_urlpatterns(urlconf.urlpatterns)

    urls = {}
    for view, path, reverse_name in view_infos:

        try:
            reverse(reverse_name)
        except NoReverseMatch:
            continue

        if path.split("/")[0] in exclude:
            continue

        import_path = view.__module__.split(".")

        if import_path[0] != PROJECT_NAME:
            continue

        app_name = import_path[1].capitalize()
        link_name = reverse_name.split(":")[-1].capitalize()

        if app_name in urls:
            urls[app_name].append((link_name, reverse_name))
        else:
            urls[app_name] = [(link_name, reverse_name)]

    documentation = []

    if "espressodb.documentation" in settings.INSTALLED_APPS:
        for app_slug, app in get_apps_slug_map().items():
            documentation.append((app_slug, get_app_name(app)))

    context = {"urls": urls, "documentation": documentation}

    return context


def render_field(field: Field) -> str:
    """Returns verbose descriptor of model field

    Arguments:
        field: The field to render.
    """
    optional = "(Optional) " if field.null else ""
    return f"{field.name}=..., # {optional}{Truncator(field.help_text).words(12)}"


def render_fields(fields: List[Field]) -> List[str]:
    """Renders fields to string.

    Arguments:
        fields: The fields to render.

    Sorts fields by being optional or not.
    """
    descriptions = []
    optional_descriptions = []
    for field in fields:
        text = render_field(field)
        if field.null:
            optional_descriptions.append(text)
        else:
            descriptions.append(text)

    return descriptions + optional_descriptions


@register.inclusion_tag("tree-to-python.html")
def render_tree(tree: Dict[str, str], root: str) -> Dict[str, str]:
    """Renders a model population tree to Python code.

    Arguments:
        tree: The column names ForeignKey dependency tree of the root model.
        root: The name of the root model.

    Returns:
        Context containing the Python code unde key ``content``.

    Uses the template ``tree-to-python.html``.
    """
    content = ""
    models = {}

    labels = set(tree.values())
    labels.add(root)

    for label in labels:
        model = MODELS[label]
        module = model.__module__
        cls = model.__name__
        app = model._meta.app_label  # pylint: disable=W0212
        name = f"{app}_{cls}"
        content += f"from {module} import {cls} as {name}\n"
        models[label] = (name, model)

    content += "\n"

    for name, label in list(tree.items())[::-1]:
        cls, model = models[label]
        fields = model.get_open_fields()
        args = "\n\t".join(render_fields(fields))
        name = name.replace(".", "_")
        content += f"{name} = {cls}.get_or_create(\n\t{args}\n)\n\n"

    cls, model = models[root]
    fields = model.get_open_fields()

    args = "\n\t".join(render_fields(fields))
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
    return (f"{user}@" if user else " ") + f"{name}"


@register.simple_tag
def project_name() -> str:
    """Returns name of the project
    """
    return PROJECT_NAME
