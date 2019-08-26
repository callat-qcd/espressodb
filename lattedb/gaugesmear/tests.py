"""Tests of Gauge Smear tables
"""
import logging

from django.test import TestCase

from lattedb.gaugesmear.models import WilsonFlow
from lattedb.gaugesmear.models import GaugeSmear

LOGGER = logging.getLogger("base")


class GaugeSmearTestCase(TestCase):
    """Tests for WilsonFlow gaguge smear table
    """

    cls = WilsonFlow
    parameters = {"flowtime": 1.0, "flowstep": 100}

    def test_get_or_create_from_parameters(self):
        """Tests get or create from parameters method

        Creates an instance and checks attributes.
        """

        WilsonFlow.get_or_create_from_parameters(self.parameters)

        gaugesmears = GaugeSmear.objects.all()
        for gaugesmear in gaugesmears:
            self.assertIsInstance(gaugesmear.specialization, WilsonFlow)
            for key, val in self.parameters.items():
                if key in WilsonFlow.__dict__:
                    self.assertEqual(val, getattr(gaugesmear.specialization, key))
