"""Additional in template functions for the lattedb module
"""
from django import template


register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("progress-bar.html")
def render_progress_bar(danger, warning, info, success):
    context = {"danger": danger, "warning": warning, "info": info, "success": success}

    return context
