"""Helper classes for setting up an admin page on start
"""
from typing import Optional, List, Tuple

from logging import getLogger

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db import models


from espressodb.base.models import Base
from espressodb.base.utilities.apps import get_project_apps


LOGGER = getLogger("espressodb")


class BaseAdmin(admin.ModelAdmin):
    """Extension to regular :class:`admin.ModelAdmin` which stores ``user`` as request
    logged in user on default.
    """

    readonly_fields = ("user",)

    def save_model(self, request, obj, form, change):
        """Overwrites ``obj.user`` with ``request.user`` before actual save.
        """
        obj.user = request.user
        super(BaseAdmin, self).save_model(request, obj, form, change)


class ListViewAdmin(admin.ModelAdmin):
    """List view admin which displays all model fields.

    Attributes:
        search_fields:
            The fields which are searchable on the admin page.
            Does only render fields which are present in ``list_display``
        list_display:
            The fields to display as a column on the admin page.
            Defaults to ``["id", "instance_name", ..., "tag"]`` where ``...`` are
            the model default fields.
        list_display_links:
            The fields which will be a link to the detail view.
            Defaults to ``["instance_name"]`` or ``["id"]`` or the first field in
            ``list_display`` (if the previous option are not present in
            ``list_display``).
        **kwargs:
            Kwargs for the parent init.
    """

    search_fields: Tuple[str] = ("tag", "name")
    list_display: Optional[List[str]] = None
    list_display_links: Optional[List[str]] = None
    display_instance_names: bool = True

    def __init__(  # pylint: disable=too-many-arguments
        self, model: Base, admin_site: AdminSite, **kwargs,
    ):
        """Sets the list display fields to espressodb defaults and model custom fields.
        """
        if self.list_display is None:
            self.list_display = ["id"] + (
                ["instance_name"] if self.display_instance_names else []
            )
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

        if self.list_display_links is None:
            if "instance_name" in self.list_display:
                self.list_display_links = ["instance_name"]
            elif "instance_name" in self.list_display:
                self.list_display_links = ["id"]
            else:
                self.list_display_links = self.list_display[:1]
        else:
            self.list_display_links = self.list_display_links

        self.search_fields = []
        for search_field in self.search_fields:
            if search_field in self.list_display:
                self.search_fields.append(search_field)

        super().__init__(model, admin_site, **kwargs)

    @staticmethod
    def instance_name(obj: Base) -> str:
        """Returns the name of the instance

        Arguments:
            obj: The model instance to render.
        """
        return str(obj)


def register_admins(
    app_name: str,
    exclude_models: Optional[List[str]] = None,
    admin_class: Optional[admin.ModelAdmin] = None,
):
    """Tries to load all models from this app and registers :class:`ListViewAdmin` sites.

    Arguments:
        app_name: The name of the app.
        exclude_models: Models contained in this app which should not appear on the admin
            page. Uses the class name of the model.
        admin_class: The admin model used to render the admin page.
            Defaults to :class:`ListViewAdmin`.

    Calls :meth:`admin.site.register` for all models within the specified app.
    """
    exclude_models = exclude_models or []

    apps = [app for app in get_project_apps() if app.name == app_name]

    admin_class = admin_class or ListViewAdmin

    if len(apps) == 1:
        for model in apps[0].get_models():
            if model.__name__ not in exclude_models:
                admin.site.register(model, admin_class)
    else:
        LOGGER.warning(
            "Was not able to locate app `%s`."
            " This is needed to register admin pages."
            " Is it in installed (see `settings.yaml`)?",
            app_name,
        )
