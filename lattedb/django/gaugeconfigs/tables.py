import django_tables2 as tables

from lattedb.django.gaugeconfigs.models import CloverGaugeConfig, HisqGaugeConfig


class HisqGaugeConfigTable(tables.Table):
    class Meta:
        model = HisqGaugeConfig
        exclude = ("type", "last_modified", "user", "misc", "gaugeconfig_ptr")


class CloverGaugeConfigTable(tables.Table):
    class Meta:
        model = CloverGaugeConfig
        exclude = ("type", "last_modified", "user", "misc", "gaugeconfig_ptr")
