from lattedb.django.main.views import TableView

from lattedb.django.propagator.models import Hisq
from lattedb.django.propagator.models import MobiusDWF

from lattedb.django.propagator.tables import HisqPropagatorsTable
from lattedb.django.propagator.tables import MobiusPropagatorsTable


class HisqPropagatorsTableView(TableView):
    table_class = HisqPropagatorsTable
    queryset = Hisq.objects.all()
    page_name = "Hisq propagator"


class MobiusPropagatorsTableView(TableView):
    table_class = MobiusPropagatorsTable
    queryset = MobiusDWF.objects.all()
    page_name = "Mobius propagator"
