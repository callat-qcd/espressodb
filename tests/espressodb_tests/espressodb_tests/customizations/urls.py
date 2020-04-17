"""Views for the customizations app
"""
from django.urls import path

from espressodb_tests.customizations.views import IndexView

app_name = "customizations"
urlpatterns = [path("", IndexView.as_view(), name="index")]
