# pylint: disable=missing-docstring
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "espressodb.notifications"
    verbose_name = "Notifications"
    label = "notifications"
    default_auto_field = "django.db.models.AutoField"
