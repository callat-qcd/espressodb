from django.contrib import admin
from lattedb.project.fhcompare.models.data import SourceAvg2pt
class DataAdmin(admin.ModelAdmin):
    pass

admin.site.register(SourceAvg2pt, DataAdmin)
# Register your models here.
