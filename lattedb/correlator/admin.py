"""Admin view for correlation functions
"""
from django.contrib import admin
from lattedb.base.admin import BaseAdmin
from lattedb.correlator.models import Baryon2pt


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
    """Admin which summarizes information for Baryon2pt

    Adding and changing permissions in the admin default to False because
    it is unfasible to selece e.g. propagators in very large tables.
    """

    list_display = (
        "id",
        "ensemble",
        "config",
        "tag",
        "origin",
        "parity",
        "spin_x2",
        "spin_z_x2",
        "isospin_x2",
        "isospin_z_x2",
    )
    list_filter = ("tag", EnsembleListFilter)
    list_display_links = None

    @staticmethod
    def config(obj):
        return obj.propagator0.specialization.gaugeconfig.specialization.config

    @staticmethod
    def origin(obj):
        return "(%d, %d, %d, %d)" % (
            obj.propagator0.specialization.origin_x,
            obj.propagator0.specialization.origin_y,
            obj.propagator0.specialization.origin_z,
            obj.propagator0.specialization.origin_t,
        )
    origin.short_description = "origin (x, y, z, t)"

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

    @staticmethod
    def has_add_permission(request):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return False


admin.site.register(Baryon2pt, Baryon2ptAdmin)
