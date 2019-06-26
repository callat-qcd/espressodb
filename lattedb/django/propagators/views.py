import django_tables2 as tables

from lattedb.django.propagators.models import HisqPropagators
from lattedb.django.propagators.models import MobiusPropagators

from lattedb.django.propagators.tables import HisqPropagatorsTable
from lattedb.django.propagators.tables import MobiusPropagatorsTable


class HisqPropagatorsTableView(tables.SingleTableView):
    table_class = HisqPropagatorsTable
    queryset = HisqPropagators.objects.all()
    template_name = "tables.html"
    paginator_class = tables.paginators.LazyPaginator


class MobiusPropagatorsTableView(tables.SingleTableView):
    table_class = MobiusPropagatorsTable
    queryset = MobiusPropagators.objects.all()
    template_name = "tables.html"
    paginator_class = tables.paginators.LazyPaginator
