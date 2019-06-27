"""Admin view for correlation functions
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.correlators.models import MesonTwoPoints

admin.site.register(MesonTwoPoints, BaseAdmin)


