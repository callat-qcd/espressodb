"""Admin view for propagator
"""
from django.contrib import admin

from lattedb.base.admin import BaseAdmin

from lattedb.propagator.models import OneToAll

admin.site.register(OneToAll, BaseAdmin)
