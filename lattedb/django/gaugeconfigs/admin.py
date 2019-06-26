"""Admin view for gauge configurations
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.gaugeconfigs.models import HisqGaugeConfig
from lattedb.django.gaugeconfigs.models import CloverGaugeConfig


admin.site.register(HisqGaugeConfig, BaseAdmin)
admin.site.register(CloverGaugeConfig, BaseAdmin)
