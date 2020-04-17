"""Additional in template functions for the base module.
"""
from typing import List, Dict, Tuple, Optional, Any

from django import template
from django.conf import settings
from django.db.models import ForeignKey
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
) -> List[Tuple[str, str]]:
    """Renders all app page links

    Arguments:
        exclude: The link names to exclude.

    Returns:
        Context with keys ``urls`` and ``documentation`` where each value is a list
        of Tuples with the reverse url name and display name.

    Ignores urls which do not result in a match.

    Uses the template ``link-list.html``.

    Note:
        It is possible to give class based views the ``exclude_from_nav`` flag.
        If this flag is set, the view will not be rendered.
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

        cls = None
        if hasattr(view, "view_class"):
            cls = view.view_class
        elif hasattr(view, "cls"):
            cls = view.cls
        if cls and hasattr(cls, "exclude_from_nav") and cls.exclude_from_nav:
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

    context = {"urls": urls}

    return context


@register.inclusion_tag("documentation-links.html")
def render_documentation_links() -> List[Tuple[str, str]]:
    """Renders all app documentation page links

    Returns:
        Context with keys ``urls`` and ``documentation`` where each value is a list
        of Tuples with the reverse url name and display name.

    Ignores urls which do not result in a match.

    Uses the template ``documentation-links.html``.
    """
    documentation = []

    if "espressodb.documentation" in settings.INSTALLED_APPS:
        for app_slug, app in get_apps_slug_map().items():
            documentation.append((app_slug, get_app_name(app)))

    return {"documentation": documentation}


def render_field(field: Field, instance_name: Optional[str] = None) -> str:
    """Returns verbose descriptor of model field

    Arguments:
        field:
            The field to render.
        instance_name:
            The name of model instance for which the fields are written.
            If given, automatically insert the value for FK fields.
            This assumes that the FK variables are defined before this class and follow
            the convention `columnname1_columnname2_...`.
    """
    optional = "(Optional) " if field.null else ""
    if instance_name is not None and isinstance(field, ForeignKey):
        field_value = (f"{instance_name}_" if instance_name else "") + field.name
    else:
        field_value = ""

    return (
        f"{field.name}={field_value},"
        f" # {optional}{Truncator(field.help_text).words(12)}"
    )


def render_fields(
    fields: List[Field], instance_name: Optional[str] = None
) -> List[str]:
    """Renders fields to string.

    Arguments:
        fields:
            The fields to render.
        instance_name:
            The name of model instance for which the fields are written.
            If given, automatically insert the value for FK fields.
            This assumes that the FK variables are defined before this class and follow
            the convention `column_name1_column_name2_...`.

    Sorts fields by being optional or not.
    """
    descriptions = []
    optional_descriptions = []
    for field in fields:
        text = render_field(field, instance_name=instance_name)
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

    labels = sorted(list(set(tree.values())))
    labels.append(root)

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
        name = name.replace(".", "_")
        args = "\n\t".join(render_fields(fields, instance_name=name))
        content += f"{name}, created ="
        content += f" {cls}.objects.get_or_create(\n\t{args}\n)\n\n"

    cls, model = models[root]
    fields = model.get_open_fields()

    args = "\n\t".join(render_fields(fields, instance_name=""))
    content += f"{cls.lower()}, created = {cls}.objects.get_or_create(\n\t{args}\n)"

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


@register.filter
def get_item(dictionary: Dict[str, Any], key: str) -> Any:
    """Extract key from dictionary

    Arguments:
        dictionary: The dictionary to search
        key: The key to look up

    See also: https://stackoverflow.com/a/8000091
    """
    return dictionary.get(key)
