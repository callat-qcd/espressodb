"""Admin view for propagator
"""
from django.contrib import admin

from lattedb.base.admin import BaseAdmin

from lattedb.propagator.models import Hisq
from lattedb.propagator.models import MobiusDWF

admin.site.register(Hisq, BaseAdmin)
admin.site.register(MobiusDWF, BaseAdmin)
