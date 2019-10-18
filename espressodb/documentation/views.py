"""Contains views for the documentation app.
"""
from typing import Dict, Any

from django.views.generic.base import TemplateView

from espressodb.base.utilities.apps import get_apps_slug_map


#: Maps app-slugs to apps
SLUG_MAP = get_apps_slug_map()


class DocView(TemplateView):
    """Renders the documentation page for apps present in EspressoDBs models.

    Uses :meth:`espressodb.base.utilities.apps.get_apps_slug_map` to locate apps.
    """

    #: The used template file.
    template_name = "doc-base.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Adds ``app_name`` from slug and adds all app model slugs to conext.
        """
        context = super().get_context_data(**kwargs)
        app = SLUG_MAP.get(context["app_slug"], None)

        app_name = app.name if app is not None else ""

        context["app_name"] = app_name
        context["models"] = [model.get_slug() for model in app.get_models()]

        return context
