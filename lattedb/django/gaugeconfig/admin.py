"""Admin view for gauge configurations
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin
from lattedb.django.gaugeconfig.models import Hisq

admin.site.register(Hisq, BaseAdmin)

#class HisqGaugeConfigurationsAdmin(BaseAdmin):
#    list_filter = ("nl", "nt", "short_tag")
#    list_display = [
#        field.name
#        for field in Hisq._meta.get_fields()
#        if field.name
#        not in ["gaugeconfigurations_ptr", "type", "hisq", "mobiusdwf"]
#    ]


#class CloverGaugeConfigurationsAdmin(BaseAdmin):
#    # list_filter = ("nl", "nt", "stream", "short_tag")
#    list_display = [
#        field.name
#        for field in CloverGaugeConfigurations._meta.get_fields()
#        if field.name
#        not in ["gaugeconfigurations_ptr", "type", "hisq", "mobiusdwf"]
#    ]


#admin.site.register(Hisq, HisqGaugeConfigurationsAdmin)
#admin.site.register(CloverGaugeConfigurations, CloverGaugeConfigurationsAdmin)
