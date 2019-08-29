from django.contrib import admin

# Register your models here.
from lattedb.ensemble.models import Ensemble


class Ensemble2ptAdmin(admin.ModelAdmin):
    """Admin which summarizes information for Ensemble
    """

    list_display = ("id", "short_tag", "long_tag", "n_configs")

    @staticmethod
    def n_configs(obj):
        return obj.configurations.count()


admin.site.register(Ensemble, Ensemble2ptAdmin)
