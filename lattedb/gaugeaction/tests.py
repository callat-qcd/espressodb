"""Tests of Gauge Action tables
"""
import logging

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.gaugeaction.models import LuescherWeisz

LOGGER = logging.getLogger("base")


class GaugeActionTestCase(TestCase, BaseTest):
    """Tests for LuescherWeisz gaguge action table
    """

    cls = LuescherWeisz
    parameters = {"beta": 0.1, "a_fm": 0.6, "u0": 1.2}
