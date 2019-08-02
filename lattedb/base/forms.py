"""Base forms
"""

from django import forms

from lattedb.base.utilities.models import get_lattedb_models


class TableSelectForm(forms.Form):
    table = forms.ChoiceField(choices=[(str(m), m) for m in get_lattedb_models()])
