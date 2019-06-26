"""Admin view for interaction operators
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.interactionoperators.models import LocalCurrents
from lattedb.django.interactionoperators.models import ConservedCurrents
from lattedb.django.interactionoperators.models import SpatialMoments


admin.site.register(LocalCurrents, BaseAdmin)
admin.site.register(ConservedCurrents, BaseAdmin)
admin.site.register(SpatialMoments, BaseAdmin)