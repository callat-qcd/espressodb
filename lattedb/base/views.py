"""Views for the base module
"""
from django.http import HttpResponse

from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.views import View
from django.shortcuts import render

from lattedb.base.forms import TableSelectForm
from lattedb.base.forms import CHOICES
from django.http import HttpResponseRedirect

from lattedb.base.models import Base
from lattedb.base.utilities.models import iter_tree


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
        print(self.table, type(self.table))
        return reverse_lazy("base:populate")


class PopulationView(View):
    template_name = "select_table.html"
    form_class = TableSelectForm

    def get(self, request):
        """
        """
        form = self.form_class()
        request.session["todo"] = []
        request.session["tree"] = {}
        request.session["name"] = None
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """The todo is to store the last selection and query the next.

        There are two cases:
            1. No last selection (name is None)
            2. Given last selection (name is not None)

        """
        form = self.form_class(request.POST)
        if form.is_valid():

            model = CHOICES[form.cleaned_data["table"]]
            name = request.session.get("name") or model.get_label()

            request.session["tree"][name] = model.get_label()

            tasks = iter_tree(name, model)

            for nn, mm in tasks[::-1]:
                request.session["todo"].insert(0, (nn, mm.get_label()))

            if request.session["todo"]:
                name, model = request.session["todo"].pop(0)
                request.session["name"] = name
                model = CHOICES[model]
                subset = (
                    [m.get_label() for m in model.__subclasses__()]
                    if not model is Base
                    else [model.get_label()]
                )
                form = self.form_class(subset=subset)

            else:
                return HttpResponse(str(request.session["tree"]))

        return render(request, self.template_name, {"form": form})
