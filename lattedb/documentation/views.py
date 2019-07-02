from django.views.generic.base import TemplateView

# Create your views here.


class DocView(TemplateView):

    template_name = "doc-base.html"
    app_name = "gaugeconfig"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = f"lattedb.{self.app_name}"
        context["doc_file"] = f"apps/{self.app_name}.html"
        return context
