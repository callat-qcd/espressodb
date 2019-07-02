"""Additional in template functions for the lattedb module
"""
from django import template

from django_extensions.management.commands.show_urls import Command as URLFinder

from lattedb.config.urls import urlpatterns

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list(exclude=("", "admin")):
    """Renders all links as a nested list
    """
    u = URLFinder()
    views = u.extract_views_from_urlpatterns(urlpatterns)

    urls = [view[1] for view in views if not view[1].split("/")[0] in exclude]

    print(urls)
    context = {}

    return context
