from django.views.generic.base import TemplateView

from django_tables2 import SingleTableView
from django_tables2.paginators import LazyPaginator


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TableView(SingleTableView):
    template_name = "tables.html"
    paginator_class = LazyPaginator
    page_name = None

    def get_context_data(self, **kwargs):
        """Adds the name of the app to the context
        """
        context = super().get_context_data(**kwargs)
        context["header"] = self.page_name
        return context
