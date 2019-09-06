from django.contrib import admin

from lattedb.status.models.correlator import Baryon2pt


class Baryon2ptStatusAdmin(admin.ModelAdmin):
    """Admin which summarizes information for Baryon2ptStatus

    Adding and changing permissions in the admin default to False because
    it is unfasible to selece e.g. propagators in very large tables.
    """

    list_filter = ("home", "status")
    list_display_links = None

    list_display = (
        "id",
        "barryon2pt",
        "home",
        "directory",
        "hdf5path",
        "timestamp",
        "status",
        "source_group",
    )


admin.site.register(Baryon2pt, Baryon2ptStatusAdmin)
