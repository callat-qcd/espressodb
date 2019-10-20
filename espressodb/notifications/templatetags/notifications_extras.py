"""Additional in template functions for the notifications module.
"""
from typing import Dict, Any

from django import template
from django.contrib.auth.models import User

from espressodb.notifications.models import Notification
from espressodb.notifications.models import LEVELS

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("render_notification.html")
def render_notification(
    notification: Notification, hide_close: bool = False
) -> Dict[str, Any]:
    """Renders notifications

    Arguments:
        notification:
            The notification.
        hide_close:
            Hide the has read button in view for this notfication.

    Uses template ``espressodb/notfications/templates/render_notification.html``.
    """
    context = {"notification": notification, "hide_close": hide_close}

    return context


@register.simple_tag
def bootstrap_level(level: str) -> str:
    """Maps logging levels to bootstrap levels. Defaults to light.

    Arguments:
        level: The logging level.
    """
    return {
        "DEBUG": "secondary",
        "INFO": "info",
        "WARNING": "warning",
        "ERROR": "danger",
    }.get(level.upper(), "light")


@register.inclusion_tag("render_notification_links.html")
def render_notification_links(user: User):
    """Renders notification links.

    Arguments:
        user: The currently logged in user.

    Also adds informations about notifications which are viewable by user.

    Uses template ``espressodb/notfications/templates/render_notification_links.html``.
    """
    notifications = Notification.get_notifications(user)
    notification_count = {}
    for level in LEVELS:
        notification_count[level.lower()] = notifications.filter(level=level).count()

    return {
        "total": sum(notification_count.values()),
        "user": user,
        "notification_count": notification_count,
    }
