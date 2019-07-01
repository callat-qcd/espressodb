"""Admin view for correlation functions
"""
from django.contrib import admin
from lattedb.django.base.admin import BaseAdmin
from lattedb.django.correlator.models import Meson2pt

admin.site.register(Meson2pt, BaseAdmin)
