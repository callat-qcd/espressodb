from lattedb.django.main.views import TableView

from lattedb.django.gaugeconfigurations.models import HisqGaugeConfigurations
from lattedb.django.gaugeconfigurations.models import CloverGaugeConfigurations

from lattedb.django.gaugeconfigurations.tables import HisqGaugeConfigurationsTable
from lattedb.django.gaugeconfigurations.tables import CloverGaugeConfigurationsTable


class HisqGaugeConfigurationsTableView(TableView):
    table_class = HisqGaugeConfigurationsTable
    queryset = HisqGaugeConfigurations.objects.all()
    page_name = "Hisq gauge configs"


class CloverGaugeConfigurationsTableView(TableView):
    table_class = CloverGaugeConfigurationsTable
    queryset = CloverGaugeConfigurations.objects.all()
    page_name = "Clover gauge configs"
