from lattedb.config.views import TableView

from lattedb.propagator.models import Hisq
from lattedb.propagator.models import MobiusDWF

from lattedb.propagator.tables import HisqPropagatorsTable
from lattedb.propagator.tables import MobiusPropagatorsTable


class HisqPropagatorsTableView(TableView):
    table_class = HisqPropagatorsTable
    queryset = Hisq.objects.all()
    page_name = "Hisq propagator"


class MobiusPropagatorsTableView(TableView):
    table_class = MobiusPropagatorsTable
    queryset = MobiusDWF.objects.all()
    page_name = "Mobius propagator"
