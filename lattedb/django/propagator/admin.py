"""Admin view for propagator
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.propagator.models import Hisq
from lattedb.django.propagator.models import MobiusDWF

admin.site.register(Hisq, BaseAdmin)
admin.site.register(MobiusDWF, BaseAdmin)
