"""Contains views for the documentation app

Views
-----

* :class:`.DocView`
"""
from django.views.generic.base import TemplateView

from espressodb.base.utilities.apps import get_apps_slug_map


SLUG_MAP = get_apps_slug_map()


class DocView(TemplateView):
    """Renders the documentation page for apps present in EspressoDBs models.

    Uses :meth:`espressodb.base.utilities.apps.get_apps_slug_map` to locate apps.

    Provides context for template ``doc-base.html``.
    """

    template_name = "doc-base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = SLUG_MAP.get(context["app_slug"], None)

        app_name = app.name if app is not None else ""

        context["app_name"] = app_name
        context["models"] = [model.get_slug() for model in app.get_models()]

        return context
