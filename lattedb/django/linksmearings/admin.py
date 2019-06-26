from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin

from lattedb.django.linksmearings.models import Unsmeared
from lattedb.django.linksmearings.models import WilsonFlow

# Register your models here.
admin.site.register(Unsmeared, BaseAdmin)
admin.site.register(WilsonFlow, BaseAdmin)
