"""Views for the base module
"""
from django.http import HttpResponse

from django.views.generic.edit import FormView

from lattedb.base.forms import TableSelectForm


def index(request):  # pylint: disable=W0613
    return HttpResponse("Hello, world. You're at the polls index.")


class TableSelectView(FormView):
    template_name = "select_table.html"
    form_class = TableSelectForm
    success_url = "/thanks/"
