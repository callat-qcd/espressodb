from lattedb.django.main.views import TableView

from lattedb.django.gaugeconfig.models import HisqGaugeConfigurations
from lattedb.django.gaugeconfig.models import CloverGaugeConfigurations

from lattedb.django.gaugeconfig.tables import HisqGaugeConfigurationsTable
from lattedb.django.gaugeconfig.tables import CloverGaugeConfigurationsTable


class HisqGaugeConfigurationsTableView(TableView):
    table_class = HisqGaugeConfigurationsTable
    queryset = HisqGaugeConfigurations.objects.all()
    page_name = "Hisq gauge configs"


class CloverGaugeConfigurationsTableView(TableView):
    table_class = CloverGaugeConfigurationsTable
    queryset = CloverGaugeConfigurations.objects.all()
    page_name = "Clover gauge configs"
