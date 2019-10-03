"""Loads the NotificationsView
"""

from django.urls import path

from espressodb.notifications.views import NotificationsView, HasReadView

app_name = "notifications"
urlpatterns = [
    path(r"", NotificationsView.as_view(), name="notifications-list"),
    path(
        r"debug/",
        NotificationsView.as_view(level="DEBUG"),
        name="notifications-list-debug",
    ),
    path(
        r"info/", NotificationsView.as_view(level="INFO"), name="notifications-list-info"
    ),
    path(
        r"warning/",
        NotificationsView.as_view(level="WARNING"),
        name="notifications-list-warning",
    ),
    path(
        r"error/",
        NotificationsView.as_view(level="ERROR"),
        name="notifications-list-error",
    ),
    path("read/<int:pk>", HasReadView.as_view(), name="notification-read"),
]
