"""Admin view for correlation functions
"""
from django.contrib import admin
from lattedb.base.admin import BaseAdmin
from lattedb.correlator.models import Meson2pt, Baryon2pt

admin.site.register(Meson2pt, BaseAdmin)


class EnsembleListFilter(admin.SimpleListFilter):
    title = "ensemble"
    parameter_name = "ensembles"

    def lookups(self, request, model_admin):
        tags = Baryon2pt.objects.values_list(
            "propagator0__onetoall__gaugeconfig__nf211__short_tag"
        ).distinct()
        return [(key[0], key[0]) for key in tags]

    def queryset(self, request, queryset):
        return (
            queryset.filter(
                propagator0__onetoall__gaugeconfig__nf211__short_tag=self.value()
            )
            if self.value()
            else queryset
        )


class Baryon2ptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "config",
        "ensemble",
        "origin",
        "origin_t",
        "parity",
        "spin_x2",
        "spin_z_x2",
        "isospin_x2",
        "isospin_z_x2",
    )
    list_filter = ("tag", EnsembleListFilter)

    @staticmethod
    def config(obj):
        return obj.propagator0.specialization.gaugeconfig.specialization.config

    @staticmethod
    def origin(obj):
        return "(%3d, %3d, %3d)" % (
            obj.propagator0.specialization.origin_x,
            obj.propagator0.specialization.origin_y,
            obj.propagator0.specialization.origin_z,
        )

    @staticmethod
    def origin_t(obj):
        return obj.propagator0.specialization.origin_t

    @staticmethod
    def parity(obj):
        return obj.sink.specialization.parity

    @staticmethod
    def spin_x2(obj):
        return obj.sink.specialization.spin_x2

    @staticmethod
    def spin_z_x2(obj):
        return obj.sink.specialization.spin_z_x2

    @staticmethod
    def isospin_x2(obj):
        return obj.sink.specialization.isospin_x2

    @staticmethod
    def isospin_z_x2(obj):
        return obj.sink.specialization.isospin_z_x2

    @staticmethod
    def ensemble(obj):
        return obj.propagator0.specialization.gaugeconfig.specialization.short_tag


admin.site.register(Baryon2pt, Baryon2ptAdmin)
