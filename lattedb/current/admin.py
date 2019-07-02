"""Admin view for interaction operators
"""
from django.contrib import admin

from lattedb.base.admin import BaseAdmin
from lattedb.current.models import Local

admin.site.register(Local, BaseAdmin)
