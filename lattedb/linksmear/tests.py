"""Tests of Gauge Smear tables
"""
import logging

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.linksmear.models import WilsonFlow

LOGGER = logging.getLogger("base")


class LinkSmearTestCase(TestCase, BaseTest):
    """Tests for WilsonFlow gaguge smear table
    """

    cls = WilsonFlow
    parameters = {"flowtime": 1.0, "flowstep": 100}
