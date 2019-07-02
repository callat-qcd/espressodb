"""Admin view for correlation functions
"""
from django.contrib import admin
from lattedb.base.admin import BaseAdmin
from lattedb.correlator.models import Meson2pt

admin.site.register(Meson2pt, BaseAdmin)
