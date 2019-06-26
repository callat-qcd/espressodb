from lattedb.django.main.views import TableView

from lattedb.django.gaugeconfigs.models import HisqGaugeConfig
from lattedb.django.gaugeconfigs.models import CloverGaugeConfig

from lattedb.django.gaugeconfigs.tables import HisqGaugeConfigTable
from lattedb.django.gaugeconfigs.tables import CloverGaugeConfigTable


class HisqGaugeConfigTableView(TableView):
    table_class = HisqGaugeConfigTable
    queryset = HisqGaugeConfig.objects.all()
    page_name = "Hisq gauge configs"


class CloverGaugeConfigTableView(TableView):
    table_class = CloverGaugeConfigTable
    queryset = CloverGaugeConfig.objects.all()
    page_name = "Clover gauge configs"
