"""Views for the base module
"""
from django.http import HttpResponse

from django.views import View
from django.shortcuts import render

from lattedb.base.forms import ModelSelectForm
from lattedb.base.forms import MODELS

from lattedb.base.models import Base
from lattedb.base.utilities.models import iter_tree


def index(request):  # pylint: disable=W0613, C0111
    return HttpResponse("Hello, world. You're at the polls index.")


class PopulationView(View):
    """View which queries the user for creating a tree for a selected table.
    """

    template_name = "select_table.html"
    form_class = ModelSelectForm

    def get(self, request):
        """Initializes from which queries user which table he wants to populate.

        This starts the parsing of the tree.
        """
        form = self.form_class()
        request.session["todo"] = []
        request.session["tree"] = {}
        request.session["name"] = None
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):  # pylint: disable=W0613
        """Processes the selected model, pops the next task and adds its subclasses
        to todo. Once the todo list is empty, it returns the tree.

        This view uses cookies for creating the query.
        """
        form = self.form_class(request.POST)
        if form.is_valid():

            model = form.get_model()
            name = request.session.get("name") or model.get_label()

            request.session["tree"][name] = model.get_label()

            tasks = iter_tree(name, model)

            for nn, mm in tasks[::-1]:
                request.session["todo"].insert(0, (nn, mm.get_label()))

            if request.session["todo"]:
                name, model = request.session["todo"].pop(0)
                request.session["name"] = name
                model = MODELS[model]
                subset = (
                    [m.get_label() for m in model.__subclasses__()]
                    if not model is Base
                    else [model.get_label()]
                )
                form = self.form_class(subset=subset)

            else:
                return HttpResponse(str(request.session["tree"]))

        return render(request, self.template_name, {"form": form})
