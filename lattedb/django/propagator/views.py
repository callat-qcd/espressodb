from lattedb.django.main.views import TableView

from lattedb.django.propagator.models import HisqPropagators
from lattedb.django.propagator.models import MobiusPropagators

from lattedb.django.propagator.tables import HisqPropagatorsTable
from lattedb.django.propagator.tables import MobiusPropagatorsTable


class HisqPropagatorsTableView(TableView):
    table_class = HisqPropagatorsTable
    queryset = HisqPropagators.objects.all()
    page_name = "Hisq propagator"


class MobiusPropagatorsTableView(TableView):
    table_class = MobiusPropagatorsTable
    queryset = MobiusPropagators.objects.all()
    page_name = "Mobius propagator"
