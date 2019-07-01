"""Admin view for propagator
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.propagator.models import HisqPropagators
from lattedb.django.propagator.models import HisqPropagatorsSimulationDetail
from lattedb.django.propagator.models import MobiusPropagators
from lattedb.django.propagator.models import MobiusPropagatorsSimulationDetail
#from lattedb.django.propagator.models import CloverPropagators

admin.site.register(HisqPropagators, BaseAdmin)
admin.site.register(HisqPropagatorsSimulationDetail, BaseAdmin)
admin.site.register(MobiusPropagators, BaseAdmin)
admin.site.register(MobiusPropagatorsSimulationDetail, BaseAdmin)
#admin.site.register(CloverPropagators, BaseAdmin)
