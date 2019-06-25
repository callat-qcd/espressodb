"""Admin view for propagators
"""
from django.contrib import admin

from base.admin import BaseAdmin

from propagators.models import HisqPropagator
from propagators.models import CloverPropagator

admin.site.register(HisqPropagator, BaseAdmin)
admin.site.register(CloverPropagator, BaseAdmin)
