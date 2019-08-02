"""Views for the base module
"""
from django.http import HttpResponse

from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from lattedb.base.forms import TableSelectForm


def index(request):  # pylint: disable=W0613
    return HttpResponse("Hello, world. You're at the polls index.")


class TableSelectView(FormView):
    template_name = "select_table.html"
    form_class = TableSelectForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = None

    def form_valid(self, form):
        self.table = form.cleaned_data["table"]
        return super().form_valid(form)

    def get_success_url(self):
        print(self.table)
        return reverse_lazy("base:populate")
