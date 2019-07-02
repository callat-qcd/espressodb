"""Additional in template functions for the lattedb module
"""
import os
from django import template
from django.urls import reverse

from django_extensions.management.commands.show_urls import Command as URLFinder

from lattedb.config.urls import urlpatterns
from lattedb.config.settings import PROJECT_APPS, BASE_DIR

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("link-list.html")
def render_link_list(exclude=("", "base", "admin", "documentation")):
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

        app_name = import_path[1].capitalize()
        link_name = reverse_name.split(":")[-1].capitalize()

        if app_name in urls:
            urls[app_name].append((link_name, reverse_name))
        else:
            urls[app_name] = [(link_name, reverse_name)]

    if "lattedb.documentation" in PROJECT_APPS:
        documentation = []
        for app_name in PROJECT_APPS:
            app_name = app_name.split(".")[-1]
            if app_name in exclude:
                continue

            if os.path.exists(
                os.path.join(
                    BASE_DIR, "documentation", "templates", "apps", app_name + ".html"
                )
            ):
                documentation.append((app_name.capitalize(), app_name))

    print(documentation)

    context = {"urls": urls, "documentation": documentation}

    return context
