"""Base forms
"""

from django import forms

from lattedb.base.utilities.models import get_lattedb_models
from lattedb.base.models import Base

CHOICES = {m.get_label(): m for m in get_lattedb_models()}


class TableSelectForm(forms.Form):
    table = forms.ChoiceField(choices=[(m, m) for m in CHOICES])

    def get_table(self):
        key = ""
        return CHOICES[key]

    def __init__(self, *args, subset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if subset:
            self.fields["table"].choices = [
                (key, val)
                for key, val in self.fields["table"].choices
                if key in subset and key != Base
            ]
