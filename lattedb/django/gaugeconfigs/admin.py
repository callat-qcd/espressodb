"""Admin view for gauge configurations
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.gaugeconfigs.models import HisqGaugeConfig
from lattedb.django.gaugeconfigs.models import CloverGaugeConfig


class HisqGaugeConfigAdmin(BaseAdmin):
    list_filter = ("nl", "nt", "stream", "short_tag")
    list_display = [
        field.name
        for field in HisqGaugeConfig._meta.get_fields()
        if field.name
        not in ["gaugeconfig_ptr", "type", "hisqpropagators", "mobiuspropagators"]
    ]


class CloverGaugeConfigAdmin(BaseAdmin):
    # list_filter = ("nl", "nt", "stream", "short_tag")
    list_display = [
        field.name
        for field in CloverGaugeConfig._meta.get_fields()
        if field.name
        not in ["gaugeconfig_ptr", "type", "hisqpropagators", "mobiuspropagators"]
    ]


admin.site.register(HisqGaugeConfig, HisqGaugeConfigAdmin)
admin.site.register(CloverGaugeConfig, CloverGaugeConfigAdmin)
