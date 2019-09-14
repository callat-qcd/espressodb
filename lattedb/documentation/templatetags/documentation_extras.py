"""Additional in template functions for the lattedb module
"""
from django import template

from lattedb.base.utilities.models import get_apps_slug_map

register = template.Library()  # pylint: disable=C0103

# Create your views here.

SLUG_MAP = get_apps_slug_map()


@register.inclusion_tag("model-doc.html")
def render_documentation(app_slug: str, model_slug: str):
    """Renders documentation of model
    """
    app = SLUG_MAP.get(app_slug, None)
    model_choices = (
        [model for model in app.get_models() if model.get_label() == model_slug]
        if app is not None
        else []
    )
    model = model_choices[0] if len(model_choices) == 1 else None

    fields = {}
    for field in model.get_open_fields():
        fields[field.name] = {
            "name": field.name,
            "optional": field.null,
            "default": field.default if field.has_default() else None,
            "help": field.help_text,
            "type": field.get_internal_type(),
        }

    context = {
        "name": model.__name__,
        "module": model.__module__,
        "doc": model.__module__,
        "base": model.__base__,
        "columns": fields,
        "app_slug": app_slug,
        "model_slug": model_slug,
    }

    return context
