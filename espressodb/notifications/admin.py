from django.contrib import admin

from espressodb.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "level", "title", "content", "tag")
    list_filter = ("level", "tag")
