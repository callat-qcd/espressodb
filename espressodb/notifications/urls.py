"""Loads the NotificationsView
"""

from django.urls import path

from espressodb.notifications.views import NotificationsView

app_name = "notifications"
urlpatterns = [path(r"", NotificationsView.as_view(), name="notifications-list")]
