"""Admin view for correlation functions
"""
from django.contrib import admin
from lattedb.django.base.admin import BaseAdmin
from lattedb.django.correlators.models import MesonTwoPoints
from lattedb.django.correlators.models import MesonTwoPointsSimulationDetail

admin.site.register(MesonTwoPoints, BaseAdmin)
admin.site.register(MesonTwoPointsSimulationDetail, BaseAdmin)
