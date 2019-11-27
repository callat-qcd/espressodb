# pylint: disable=missing-docstring
from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "espressodb.base"
    verbose_name = "EspressoDB Base"
    label = "base"

    def ready(self):
        """Loads signals from espressodb
        """
        import espressodb.base.signals  # pylint: disable=W0611
