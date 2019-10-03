"""Additional in template functions for the espressodb module
"""
from django import template

from espressodb.notifications.models import Notification

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("render_notification.html")
def render_notification(notification: Notification, hide_close: bool = False):
    """Renders notification
    """
    context = {"notification": notification, "hide_close": hide_close}

    return context


@register.simple_tag
def bootstrap_level(level: str) -> str:
    """Maps logging levels to bootstrap levels. Defaults to light.
    """
    return {
        "DEBUG": "secondary",
        "INFO": "info",
        "WARNING": "warning",
        "ERROR": "danger",
    }.get(level, "light")
