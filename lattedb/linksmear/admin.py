from django.contrib import admin

from lattedb.base.admin import BaseAdmin

from lattedb.linksmear.models import Unsmeared
from lattedb.linksmear.models import WilsonFlow

# Register your models here.
admin.site.register(Unsmeared, BaseAdmin)
admin.site.register(WilsonFlow, BaseAdmin)
