"""Admin view for propagators
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.propagators.models import HisqPropagators
from lattedb.django.propagators.models import MobiusPropagators
#from lattedb.django.propagators.models import CloverPropagators

admin.site.register(HisqPropagators, BaseAdmin)
admin.site.register(MobiusPropagators, BaseAdmin)
#admin.site.register(CloverPropagators, BaseAdmin)
