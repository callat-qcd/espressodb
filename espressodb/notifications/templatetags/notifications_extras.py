"""Additional in template functions for the espressodb module
"""
from django import template

from espressodb.notifications.models import Notification

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("render_notification.html")
def render_notification(notification: Notification):
    """Renders notification
    """
    context = {"notification": notification}

    return context
