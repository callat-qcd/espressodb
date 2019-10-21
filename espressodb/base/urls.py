# pylint: disable=invalid-name, line-too-long
"""Contains url patterns for the base app. This includes the index view.

The URL-app name is ``base``.

+-----------------+----------------------+-----------------------------------------------------+
| Name            | Path                 | View                                                |
+=================+======================+=====================================================+
| index           | ``""``               | :class:`espressodb.base.views.IndexView`            |
+-----------------+----------------------+-----------------------------------------------------+
| populate        | ``populate/``        | :class:`espressodb.base.views.PopulationView`       |
+-----------------+----------------------+-----------------------------------------------------+
| populate-result | ``populate-result/`` | :class:`espressodb.base.views.PopulationResultView` |
+-----------------+----------------------+-----------------------------------------------------+
"""
from django.urls import path

from espressodb.base import views

urlpatterns = []

app_name = "base"
urlpatterns += [
    path("", views.IndexView.as_view(), name="index"),
    path("populate/", views.PopulationView.as_view(), name="populate"),
    path(
        "populate-result/", views.PopulationResultView.as_view(), name="populate-result"
    ),
]
