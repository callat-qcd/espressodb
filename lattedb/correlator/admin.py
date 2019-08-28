"""Admin view for correlation functions
"""
from django.contrib import admin
from lattedb.base.admin import BaseAdmin
from lattedb.correlator.models import Meson2pt, Baryon2pt

admin.site.register(Meson2pt, BaseAdmin)


class Baryon2ptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "view_propagator0",
        "view_propagator1",
        "view_propagator2",
        "view_source",
        "view_sink",
    )

    @staticmethod
    def view_propagator0(obj):
        return str(obj.propagator0.specialization)

    @staticmethod
    def view_propagator1(obj):
        return str(obj.propagator1.specialization)

    @staticmethod
    def view_propagator2(obj):
        return str(obj.propagator2.specialization)

    @staticmethod
    def view_source(obj):
        return str(obj.source.specialization)

    @staticmethod
    def view_sink(obj):
        return str(obj.sink.specialization)


admin.site.register(Baryon2pt, Baryon2ptAdmin)
