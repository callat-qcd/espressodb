from django.contrib import admin

from lattestructs.models import HisqGaugeConfig
from lattestructs.models import CloverGaugeConfig
from lattestructs.models import HisqPropagator
from lattestructs.models import CloverPropagator


class HisqGaugeConfigAdmin(admin.ModelAdmin):
    pass


class CloverGaugeConfigAdmin(admin.ModelAdmin):
    pass


class HisqPropagatorAdmin(admin.ModelAdmin):
    pass


class CloverPropagatorAdmin(admin.ModelAdmin):
    pass


admin.site.register(HisqGaugeConfig, HisqGaugeConfigAdmin)
admin.site.register(CloverGaugeConfig, CloverGaugeConfigAdmin)
admin.site.register(HisqPropagator, HisqPropagatorAdmin)
admin.site.register(CloverPropagator, CloverPropagatorAdmin)
