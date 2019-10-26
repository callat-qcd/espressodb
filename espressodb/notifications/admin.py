"""Admin pages for the notifications app.
"""
from django.contrib import admin

from espressodb.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin page for the :class:`espressodb.notifications.models.Notification` model.
    """

    list_display = ("timestamp", "level", "title", "content", "tag")
    list_filter = ("level", "tag")
