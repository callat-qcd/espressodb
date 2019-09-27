"""Views for the base module
"""
from typing import List
from typing import Dict
from typing import Any
from typing import Tuple

from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect

from espressodb.base.forms import ModelSelectForm
from espressodb.base.forms import MODELS

from espressodb.base.models import Base
from espressodb.base.utilities.models import iter_tree


class IndexView(TemplateView):

    template_name = "index.html"


class PopulationView(View):
    """View which queries the user for creating a tree for a selected table.
    """

    template_name = "select-table.html"
    form_class = ModelSelectForm

    def get(self, request):
        """Initializes from which queries user which table he wants to populate.

        This starts the parsing of the tree.
        """
        form = self.form_class()
        request.session["todo"] = []
        request.session["tree"] = {}
        request.session["column"] = None
        request.session["root"] = None
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):  # pylint: disable=W0613
        """Processes the selected model, pops the next task and adds its subclasses
        to todo. Once the todo list is empty, it returns the tree.

        This view uses cookies for creating the query.
        """
        form = self.form_class(request.POST)
        if form.is_valid():

            model = self.get_choice(form, request.session)
            column_label, model_subset = self.get_next(
                model, request.session, form.get_parse_tree()
            )

            if column_label:
                form = self.form_class(subset=model_subset, name=column_label)
            else:
                return redirect("populate-result")

        return render(request, self.template_name, {"form": form})

    @staticmethod
    def get_choice(form: ModelSelectForm, session: Dict[str, Any]) -> Base:
        """Reads form and sets root model if not present.
        """
        model = form.get_model()
        root = session.get("root", None)

        if root is None:
            session["root"] = model.get_label()

        return model

    def get_next(
        self, model: Base, session: Dict[str, Any], parse_tree: bool = True
    ) -> Tuple[Base, List[Base]]:
        """
        """
        # Add current model to tree
        column = session.get("column", None)
        if column:
            session["tree"][column] = model.get_label()

        # Add dpendencies of sub model to tree
        if parse_tree:
            for sub_column, sub_model in iter_tree(model, column):
                session["todo"].insert(0, (sub_column, sub_model.get_label()))

        if session["todo"]:

            # Get next to do
            next_column, next_label = session["todo"].pop(0)
            session["column"] = next_column
            next_model = MODELS[next_label]
            next_model_choices = [next_model.get_label()]
            if next_model.__subclasses__():
                next_model_choices = [m.get_label() for m in next_model.__subclasses__()]

            # Make choice automatically if only one choice
            if len(next_model_choices) == 1:
                next_column, next_model_choices = self.get_next(
                    MODELS[next_model_choices[0]], session, parse_tree=parse_tree
                )

        else:
            next_column = next_model_choices = None

        return next_column, next_model_choices


class PopulationResultView(View):
    template_name = "present-populate.html"

    def get(self, request):
        """Initializes from which queries user which table he wants to populate.

        This starts the parsing of the tree.
        """
        for key in ["todo", "column"]:
            if key in request.session:
                request.session.pop(key)

        context = (
            {"root": request.session.get("root"), "tree": request.session.get("tree")}
            if "root" in request.session and "tree" in request.session
            else {}
        )
        return render(request, self.template_name, context)
