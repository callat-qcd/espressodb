"""Additional in template functions for the lattedb module
"""
from django import template

from django_extensions.management.commands.show_urls import Command as URLFinder

from lattedb.config.urls import urlpatterns

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list(exclude=("", "base", "admin")):
    """Renders all links as a nested list
    """
    u = URLFinder()
    view_infos = u.extract_views_from_urlpatterns(urlpatterns)

    urls = {}
    for view, path, reverse_name in view_infos:

        if path.split("/")[0] in exclude:
            continue

        import_path = view.__module__.split(".")

        if import_path[0] != "lattedb":
            continue

        print(view, path, reverse_name)

        app_name = import_path[1].capitalize()
        link_name = reverse_name.split(":")[-1].capitalize()

        if app_name in urls:
            urls[app_name].append((link_name, reverse_name))
        else:
            urls[app_name] = [(link_name, reverse_name)]

    print(urls)
    context = {"urls": urls}

    return context
