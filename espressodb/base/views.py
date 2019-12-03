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
from espressodb.base.utilities.markdown import convert_string


class IndexView(TemplateView):
    """The default index view.
    """

    #: The used template file.
    template_name = "index.html"


class PopulationView(View):
    """View which guides the user in creating a nested model population script.

    This view queries which model the user wants to populate.
    If the model has Foreign Keys, it queries the user which table to select in case
    there are multiple options (in case there is just one, this table will be selceted).

    The logic works as follows, the root table might depend on other tables which might
    depend on other tables as well.
    This defines a tree of tables where each ForeignKey of the current table column needs
    to be matched against possible table options.
    This view iterates user choices and queries the user for open column-table pairs.

    This view uses the request ``session`` (e.g, cookies) to store previously selected
    values.
    Thus there exist no unique link for the view.

    The following keywords are used to identify the nested dependencies:
        * ``root`` - the model on top of the tree (e.g, the first choosen table)
        * ``todo`` - tables which need to be specified by the user to parse the tree
        * ``tree`` - cloumn-tables pairs which have been specified by the user.
          The column name reflects recursice column names. See the ``column`` key.
        * ``column`` - the current column name. This name might be a combination of
          nested column dependencies like ``columnA_columnB`` and so on.

    Both the ``todo`` and ``tree`` lists are odered such that models are created bottom
    up to create an executable script.

    Warning:
        The querying logic breaks if the user navigates backwards.
    """

    #: The used template file.
    template_name = "select-table.html"
    #: The used form.
    form_class = ModelSelectForm

    def get(self, request):
        """Initializes from which queries the user about tables for population.

        Initializes the ``root``, ``todo``, ``tree`` and ``column`` ``session`` context
        to empty values.
        """
        form = self.form_class()
        request.session["help"] = {}
        request.session["todo"] = []
        request.session["tree"] = {}
        request.session["column"] = None
        request.session["root"] = None
        request.session.modified = True  # tell django to store changes
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):  # pylint: disable=W0613
        """Processes the selected model and prepares the next choices.

        The ``session`` context is modified in the following way:

        1. If the form is valid, extract the current column-table choice using
           :meth:`PopulationView.get_choice`.
        2. Get the next column-table option the user has to specify using
           :meth:`PopulationView.get_next`.
        3. Return a new column-table from for the user to answer if not done yet.
        4. Redirect to :class:`PopulationResultView` if there is nothing to do.
        """
        form = self.form_class(request.POST)
        if form.is_valid():

            model = self.get_choice(form, request.session)
            column_label, model_subset = self.get_next(
                model, request.session, form.get_parse_tree()
            )

            if column_label:
                form = self.form_class(
                    subset=model_subset,
                    name=column_label,
                    help_text=request.session["help"].get(column_label),
                )
            else:
                return redirect("base:populate-result")

        return render(request, self.template_name, {"form": form})

    @staticmethod
    def get_choice(form: ModelSelectForm, session: Dict[str, Any]) -> Base:
        """Reads form and sets ``root`` model if not present in ``session``.

        Arguments:
            form: The valid form.
            session: The current session. Will be updated if ``root is None``.
        """
        model = form.get_model()
        root = session.get("root", None)

        if root is None:
            session["root"] = model.get_label()
            session.modified = True  # tell django to store changes

        return model

    def get_next(
        self, model: Base, session: Dict[str, Any], parse_tree: bool = True
    ) -> Tuple[Base, List[Base]]:
        """Updates the ``todo`` list by working through present entries.

        Arguments:
            model: The current ``column`` model.
            parse_tree:
                Adds possible user choices for dependencies of current
                ``column`` if True to ``todo`` list.
            session: The current session. Will be updated if ``root is None``.

        This method works the following way:

        1. Add current select model to tree if present.
        2. Parse the tree of the current model if ``parse_tree`` using
           :meth:`espressodb.base.utilities.models.iter_tree`.
        3. Update ``todo`` if present (see below) else return (render result view).

        The ``todo`` update works as follows:

        1. Pop the first entry in the ``todo`` list and add this entry to ``column``
        2. Find possible tables which can be chosen for this model. This modifies the
           ``column`` context.
        3. If there is more then one choices, ask the user which model to select.
           This means returning back to the form query page.
        4. Pick the only option if there is just one choice, and recursively call this
           method for this choice.
        """
        # Add current model to tree
        column = session.get("column", None)
        if column:
            session["tree"][column] = {
                "label": model.get_label(),
                "doc_url": model.get_doc_url(),
            }

        # Add dpendencies of sub model to tree
        if parse_tree:
            for sub_column, sub_model in iter_tree(model, column):
                session["todo"].insert(0, (sub_column, sub_model.get_label()))
                session["help"][sub_column] = [
                    convert_string(field.help_text)
                    for field in model.get_open_fields()
                    if field.name == sub_column.split(".")[-1]
                ][0]

        if session["todo"]:

            # Get next to do
            next_column, next_label = session["todo"].pop(0)
            session["column"] = next_column
            next_model = MODELS[next_label]
            next_model_choices = [next_model.get_label()]

            if next_model.__subclasses__():
                next_model_choices = [
                    m.get_label() for m in next_model.__subclasses__()
                ]

            # Make choice automatically if only one choice
            if len(next_model_choices) == 1:
                next_column, next_model_choices = self.get_next(
                    MODELS[next_model_choices[0]], session, parse_tree=parse_tree
                )

        else:
            next_column = next_model_choices = None

        session.modified = True  # tell django to store changes
        return next_column, next_model_choices


class PopulationResultView(View):
    """View which presents the result of the population query process.

    This view generates a Python script which can be used to query or create nested
    models once the user has filled out columns in script.
    """

    #: The used template file.
    template_name = "present-populate.html"

    def get(self, request):
        """Presents the population results.

        Modifies the ``session``.
        E.g., the ``todo`` and ``column`` entries are deleted.
        """
        for key in ["todo", "column", "help"]:
            if key in request.session:
                request.session.pop(key)
                request.session.modified = True  # tell django to store changes

        context = (
            {
                "root": request.session.get("root"),
                "tree": {
                    key: value["label"]
                    for key, value in request.session.get("tree", {}).items()
                },
            }
            if "root" in request.session and "tree" in request.session
            else {}
        )

        return render(request, self.template_name, context)
