"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.interpolatorsmear.models import Gaussian


class InterpolatorSmearTestCase(TestCase, BaseTest):

    cls = Gaussian
    parameters = {"description": "Funny", "radius": 1.0, "step": 2}
