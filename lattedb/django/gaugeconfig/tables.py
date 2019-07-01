import django_tables2 as tables

from lattedb.django.gaugeconfig.models import CloverGaugeConfigurations, HisqGaugeConfigurations


class HisqGaugeConfigurationsTable(tables.Table):
    class Meta:
        model = HisqGaugeConfigurations
        exclude = ("type", "last_modified", "user", "misc", "gaugeconfigurations_ptr")


class CloverGaugeConfigurationsTable(tables.Table):
    class Meta:
        model = CloverGaugeConfigurations
        exclude = ("type", "last_modified", "user", "misc", "gaugeconfigurations_ptr")
