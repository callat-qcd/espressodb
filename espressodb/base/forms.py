"""Base forms
"""
from typing import Optional
from typing import List

from django import forms

from espressodb.base.utilities.models import get_espressodb_models

MODELS = {m.get_label(): m for m in get_espressodb_models()}


class ModelSelectForm(forms.Form):
    """Form which les the user select app models

    .. note:
        Can only select models which are not the parent of another model.
    """

    model = forms.ChoiceField(
        choices=[
            (label, label)
            for label, model in MODELS.items()
            if not model.__subclasses__()
        ]
    )
    parse_tree = forms.BooleanField(
        initial=True,
        required=False,
        help_text="Identifies foreign keys for the model and queries their type.",
    )

    def get_model(self):
        """Returns the model for given selection.
        """
        return MODELS[self.cleaned_data["model"]]

    def get_parse_tree(self):
        """Returns selection for parse tree
        """
        return self.cleaned_data["parse_tree"]

    def __init__(
        self,
        *args,
        subset: Optional[List[str]] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """Initializes the form

        Limits choice to models which do not have `Base` as their direct ancestor.

        **Arguments**
            subset: Optional[List[str]] = None
                List of strings which model must match to be present in this form
        """
        super().__init__(*args, **kwargs)

        if subset:
            self.fields["model"].choices = [
                (key, val) for key, val in self.fields["model"].choices if key in subset
            ]
        if name:
            self.fields["model"].label = name
