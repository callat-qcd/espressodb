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

    def get_context_data(self, **kwargs):
        """Adds the name of the app to the context
        """
        context = super().get_context_data(**kwargs)
        context["header"] = "Hisq gauge configs"
        return context


class CloverGaugeConfigTableView(tables.SingleTableView):
    table_class = CloverGaugeConfigTable
    queryset = CloverGaugeConfig.objects.all()
    template_name = "tables.html"
    paginator_class = tables.paginators.LazyPaginator
