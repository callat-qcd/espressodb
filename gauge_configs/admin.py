"""Admin view for gauge configurations
"""
from django.contrib import admin

from base.admin import BaseAdmin

from gauge_configs.models import HisqGaugeConfig
from gauge_configs.models import CloverGaugeConfig


admin.site.register(HisqGaugeConfig, BaseAdmin)
admin.site.register(CloverGaugeConfig, BaseAdmin)
