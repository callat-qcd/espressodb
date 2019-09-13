"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.quarksmear.models import GaugeCovariantGaussian


class QuarkSmearTestCase(TestCase, BaseTest):

    cls = GaugeCovariantGaussian
    parameters = {"description": "Funny", "radius": 1.0, "step": 2}
