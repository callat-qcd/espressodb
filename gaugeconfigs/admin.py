"""Admin view for gauge configurations
"""
from django.contrib import admin

from base.admin import BaseAdmin

from gaugeconfigs.models import HisqGaugeConfig
from gaugeconfigs.models import CloverGaugeConfig


admin.site.register(HisqGaugeConfig, BaseAdmin)
admin.site.register(CloverGaugeConfig, BaseAdmin)
