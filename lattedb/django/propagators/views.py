from lattedb.django.main.views import TableView

from lattedb.django.propagators.models import HisqPropagators
from lattedb.django.propagators.models import MobiusPropagators

from lattedb.django.propagators.tables import HisqPropagatorsTable
from lattedb.django.propagators.tables import MobiusPropagatorsTable


class HisqPropagatorsTableView(TableView):
    table_class = HisqPropagatorsTable
    queryset = HisqPropagators.objects.all()
    page_name = "Hisq propagators"


class MobiusPropagatorsTableView(TableView):
    table_class = MobiusPropagatorsTable
    queryset = MobiusPropagators.objects.all()
    page_name = "Mobius propagators"
