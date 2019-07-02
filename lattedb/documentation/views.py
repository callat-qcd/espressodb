from django.views.generic.base import TemplateView

# Create your views here.


class DocView(TemplateView):

    template_name = "doc-base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = context["app_name"]
        context["header"] = f"lattedb.{app_name}"
        context["doc_file"] = f"apps/{app_name}.html"
        return context
