"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.fermionaction.models import Hisq

# Create your tests here.


class FermionActionTestCase(TestCase, BaseTest):

    cls = Hisq
    parameters = {"quark_mass": "0.1", "quark_tag": "s", "naik": 1.0}