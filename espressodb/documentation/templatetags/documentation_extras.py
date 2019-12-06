"""Additional in template functions for the documentation module
"""
from django import template
from django.template.defaultfilters import slugify
from django.urls import reverse

from espressodb.base.utilities.apps import get_apps_slug_map, get_app_name

from espressodb.base.utilities.markdown import convert_string


register = template.Library()  # pylint: disable=C0103

SLUG_MAP = get_apps_slug_map()


@register.inclusion_tag("model-doc.html")
def render_documentation(app_slug: str, model_slug: str):
    """Renders documentation of model

    Arguments:
        app_slug:
            Slug of the app to be rendered.
            Uses :meth:`espressodb.base.utilities.apps.get_apps_slug_map` to obtain
            app from app names.
        model_slug:
            Slug of the model to be rendered.


    Uses the template ``model-doc.html``.
    """
    context = {"app_slug": app_slug, "model_slug": model_slug}

    app = SLUG_MAP.get(app_slug, None)
    model_choices = (
        [model for model in app.get_models() if model.get_slug() == model_slug]
        if app is not None
        else []
    )
    model = model_choices[0] if len(model_choices) == 1 else None

    fields = {}
    if model is not None:
        for field in model.get_open_fields():

            relation = None
            if field.is_relation:
                app_slug = slugify(
                    get_app_name(
                        field.related_model._meta.app_config  # pylint: disable=W0212
                    )
                )
                relation = {
                    "model": field.related_model.__name__,
                    "doc_link": reverse(
                        "documentation:details", kwargs={"app_slug": app_slug}
                    ),
                    "model_slug": field.related_model.get_slug(),
                }

            fields[field.name] = {
                "name": field.name,
                "optional": field.null,
                "default": field.default if field.has_default() else None,
                "help": convert_string(field.help_text),
                "type": field.get_internal_type(),
                "relation": relation,
            }

        context["name"] = model.__name__
        context["module"] = model.__module__
        context["doc"] = convert_string(model.__doc__, wrap_blocks=True)
        context["base"] = model.__base__
        # For the rare case where a field name is items, prefer this key val iteration
        context["columns"] = [(key, val) for key, val in fields.items()]

    return context
