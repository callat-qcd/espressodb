"""Admin view for propagators
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.propagators.models import HisqPropagator
from lattedb.django.propagators.models import CloverPropagator

admin.site.register(HisqPropagator, BaseAdmin)
admin.site.register(CloverPropagator, BaseAdmin)
