# pylint: disable=missing-docstring
from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "espressodb.base"
    verbose_name = "EspressoDB Base"
    label = "base"
