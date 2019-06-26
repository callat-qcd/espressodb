import django_tables2 as tables

from lattedb.django.propagators.models import HisqPropagators, MobiusPropagators


class HisqPropagatorsTable(tables.Table):
    class Meta:
        model = HisqPropagators
        exclude = ("type", "last_modified", "user", "misc", "propagators_ptr")


class MobiusPropagatorsTable(tables.Table):
    class Meta:
        model = MobiusPropagators
        exclude = ("type", "last_modified", "user", "misc", "propagators_ptr")
