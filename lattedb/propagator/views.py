from lattedb.config.views import TableView

from lattedb.propagator.models import OneToAll

from lattedb.propagator.tables import OneToAllTable


class OneToAllPropagatorsTableView(TableView):
    table_class = OneToAllTable
    queryset = OneToAll.objects.all()
    page_name = "OneToAll propagator"

