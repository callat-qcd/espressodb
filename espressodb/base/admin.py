"""Helper classes for setting up an admin page on start

ToDo: needs more doc
"""
from django.contrib import admin
from django.db import models

from espressodb.base.models import Base
from espressodb.base.utilities.apps import get_project_apps

from logging import getLogger

LOGGER = getLogger("espressodb")


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(BaseAdmin, self).save_model(request, obj, form, change)


class ListViewAdmin(admin.ModelAdmin):
    """List view admin which displays all base model fields
    """

    def __init__(self, model, admin_site, **kwargs):
        """Sets the list display fields to espressodb defaults and model custom fields.

        Allows to serach the name field if any field has name in it
        """
        if "list_display" not in kwargs:
            self.list_display = ["id", "instance_name"]
            if not issubclass(model, Base):
                raise TypeError(
                    "To use the espressodb default list admin,"
                    " the model must inherit from Base"
                )
            self.list_display += [
                field.name
                for field in model.get_open_fields()
                if not isinstance(field, models.ManyToManyField)
                and field.name not in ["id", "tag"]
            ]
            self.list_display += ["tag"]

        else:
            self.list_display = kwargs["list_display"]

        if "list_display_links" not in kwargs:
            if "instance_name" in self.list_display:
                self.list_display_links = ["instance_name"]
        else:
            self.list_display_links = kwargs["list_display_links"]

        if "search_fields" not in kwargs:
            if "name" in self.list_display:
                self.search_fields = ["name"]
        else:
            self.search_fields = kwargs["search_fields"]

        super().__init__(model, admin_site)

    @staticmethod
    def instance_name(obj):
        """Returns the name of the instance
        """
        return str(obj)


def register_admins(app_name: str):
    """Tries to load all models from this app and registers ListViewAdmin sites
    """
    apps = [app for app in get_project_apps() if app.name == app_name]

    if len(apps) == 1:
        for model in apps[0].get_models():
            admin.site.register(model, ListViewAdmin)
    else:
        LOGGER.warning(
            "Was not able to locate app `%s`."
            " Is it in installed (see `settings.yaml`)?",
            app_name,
        )
