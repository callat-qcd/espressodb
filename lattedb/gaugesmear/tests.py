"""Tests of Gauge Smear tables
"""
import logging

from django.test import TestCase

from lattedb.gaugesmear.models import WilsonFlow
from lattedb.gaugesmear.models import GaugeSmear

LOGGER = logging.getLogger("base")


class WilsonFlowTestCase(TestCase):
    """Tests for WilsonFlow gaguge smear table
    """

    parameters = {"gaugesmear": {"flowtime": 1.0, "flowstep": 100}}

    def test_get_or_create_from_parameters(self):
        """Tests get or create from parameters method

        Creates an instance and checks attributes.
        """
        parameters = {}
        for pars in self.parameters.values():
            parameters.update(pars)

        WilsonFlow.get_or_create_from_parameters(parameters)

        gaugesmears = GaugeSmear.objects.all()
        for gaugesmear in gaugesmears:
            self.assertIsInstance(gaugesmear.specialization, WilsonFlow)
            for key, val in parameters.items():
                if key in WilsonFlow.__dict__:
                    self.assertEqual(val, getattr(gaugesmear.specialization, key))
