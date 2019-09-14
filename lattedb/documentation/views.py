from django.views.generic.base import TemplateView

from lattedb.base.utilities.models import get_apps_slug_map

# Create your views here.

SLUG_MAP = get_apps_slug_map()


class DocView(TemplateView):

    template_name = "doc-base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = SLUG_MAP.get(context["app_slug"], None)

        app_name = app.name if app is not None else ""

        context["app_name"] = app_name
        context["models"] = [model.get_label() for model in app.get_models()]

        return context
