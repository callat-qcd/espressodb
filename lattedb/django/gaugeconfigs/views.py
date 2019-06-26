from django.shortcuts import render

import django_tables2 as tables

from lattedb.django.gaugeconfigs.models import HisqGaugeConfig
from lattedb.django.gaugeconfigs.models import CloverGaugeConfig

from lattedb.django.gaugeconfigs.tables import HisqGaugeConfigTable
from lattedb.django.gaugeconfigs.tables import CloverGaugeConfigTable


class HisqGaugeConfigTableView(tables.SingleTableView):
    table_class = HisqGaugeConfigTable
    queryset = HisqGaugeConfig.objects.all()
    template_name = "tables.html"
    paginator_class = tables.paginators.LazyPaginator


class CloverGaugeConfigTableView(tables.SingleTableView):
    table_class = CloverGaugeConfigTable
    queryset = CloverGaugeConfig.objects.all()
    template_name = "tables.html"
    paginator_class = tables.paginators.LazyPaginator
