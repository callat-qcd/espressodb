import django_tables2 as tables

from lattedb.django.propagator.models import Hisq, MobiusDWF


class HisqPropagatorsTable(tables.Table):
    class Meta:
        model = Hisq
        exclude = ("type", "last_modified", "user", "misc", "propagators_ptr")


class MobiusPropagatorsTable(tables.Table):
    class Meta:
        model = MobiusDWF
        exclude = ("type", "last_modified", "user", "misc", "propagators_ptr")
