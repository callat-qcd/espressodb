"""Admin view for interaction operators
"""
from django.contrib import admin

from lattedb.django.base.admin import BaseAdmin
from lattedb.django.current.models import Local

admin.site.register(Local, BaseAdmin)
