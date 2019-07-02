"""Additional in template functions for the lattedb module
"""

from django import template

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list():
    """Renders all links as a nested list
    """
    context = {}
    return context
