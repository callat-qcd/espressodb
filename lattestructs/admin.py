from django.contrib import admin
from lattestructs.models import Source, Hisq, Clover, GaugeConfiguration


class SourceAdmin(admin.ModelAdmin):
    pass


class HisqAdmin(admin.ModelAdmin):
    pass


class CloverAdmin(admin.ModelAdmin):
    pass


class GaugeConfigurationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Source, SourceAdmin)
admin.site.register(Hisq, HisqAdmin)
admin.site.register(Clover, CloverAdmin)
admin.site.register(GaugeConfiguration, GaugeConfigurationAdmin)
