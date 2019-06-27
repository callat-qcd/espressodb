from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.operatorsmearings.models import GaugeInvariantGaussian

# Register your models here.
admin.site.register(GaugeInvariantGaussian, BaseAdmin)
