"""Admin view for interpolating operators
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.hadronop.models import Basak


admin.site.register(Basak, BaseAdmin)
