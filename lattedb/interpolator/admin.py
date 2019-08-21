"""Admin view for interpolating operators
"""
from django.contrib import admin

from lattedb.base.admin import BaseAdmin

from lattedb.interpolator.models import Hadron


admin.site.register(Hadron, BaseAdmin)
