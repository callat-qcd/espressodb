"""Admin view for interaction operators
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.currentop.models import Local
from lattedb.django.currentop.models import ConservedCurrents
from lattedb.django.currentop.models import SpatialMoments


admin.site.register(Local, BaseAdmin)
admin.site.register(ConservedCurrents, BaseAdmin)
admin.site.register(SpatialMoments, BaseAdmin)