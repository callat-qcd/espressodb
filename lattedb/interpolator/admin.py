"""Admin view for interpolating operators
"""
from django.contrib import admin

from lattedb.base.admin import BaseAdmin

from lattedb.interpolator.models import Basak


admin.site.register(Basak, BaseAdmin)
