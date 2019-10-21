"""Wrapper script to allow running example project tests for EspressoDB

Follows:
https://www.ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/
"""
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "my_project.config.settings"
TEST_DIR = os.path.dirname(__file__)
sys.path.insert(0, TEST_DIR)


def runtests():
    """Runs ``my_project`` tests.
    """
    from django.test.utils import get_runner
    from django.conf import settings

    test_runner = get_runner(settings)
    failures = test_runner([], verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == "__main__":
    runtests()
