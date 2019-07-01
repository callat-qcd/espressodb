"""Admin view for gauge configurations
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.gaugeconfigurations.models import HisqGaugeConfigurations
from lattedb.django.gaugeconfigurations.models import CloverGaugeConfigurations
from lattedb.django.gaugeconfigurations.models import HisqGaugeConfigurationsSimulationDetail

admin.site.register(HisqGaugeConfigurations, BaseAdmin)
admin.site.register(HisqGaugeConfigurationsSimulationDetail, BaseAdmin)
admin.site.register(CloverGaugeConfigurations, BaseAdmin)

#class HisqGaugeConfigurationsAdmin(BaseAdmin):
#    list_filter = ("nl", "nt", "short_tag")
#    list_display = [
#        field.name
#        for field in HisqGaugeConfigurations._meta.get_fields()
#        if field.name
#        not in ["gaugeconfigurations_ptr", "type", "hisqpropagators", "mobiuspropagators"]
#    ]


#class CloverGaugeConfigurationsAdmin(BaseAdmin):
#    # list_filter = ("nl", "nt", "stream", "short_tag")
#    list_display = [
#        field.name
#        for field in CloverGaugeConfigurations._meta.get_fields()
#        if field.name
#        not in ["gaugeconfigurations_ptr", "type", "hisqpropagators", "mobiuspropagators"]
#    ]


#admin.site.register(HisqGaugeConfigurations, HisqGaugeConfigurationsAdmin)
#admin.site.register(CloverGaugeConfigurations, CloverGaugeConfigurationsAdmin)
