# pylint: disable=C0103
"""Contains url patterns for the documentation app

The URL-app name is ``documentation``.


+---------+----------------------+-------------------------------------------------+
| Name    | Path                 | View                                            |
+=========+======================+=================================================+
| details | ``<slug:app_slug>/`` | :class:`espressodb.documentation.views.DocView` |
+---------+----------------------+-------------------------------------------------+
"""
from django.urls import path

from espressodb.documentation.views import DocView

app_name = "documentation"
urlpatterns = [path(r"<slug:app_slug>/", DocView.as_view(), name="details")]
