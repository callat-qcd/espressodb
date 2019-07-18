import django_tables2 as tables

from lattedb.propagator.models import OneToAll


class OneToAllTable(tables.Table):
    class Meta:
        model = OneToAll
        exclude = ("type", "last_modified", "user", "misc", "propagators_ptr")

