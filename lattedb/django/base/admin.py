from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(BaseAdmin, self).save_model(request, obj, form, change)
