from django.contrib import admin

from base.admin import BaseAdmin

from linksmearing.models import Unsmeared
from linksmearing.models import WilsonFlow

# Register your models here.
admin.site.register(Unsmeared, BaseAdmin)
admin.site.register(WilsonFlow, BaseAdmin)