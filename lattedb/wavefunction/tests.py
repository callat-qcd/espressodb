"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.wavefunction.models import Hadron


class HadronTestCase(TestCase, BaseTest):

    cls = Hadron
    parameters = {
        "description": "Sad",
        "strangeness": 1000,  # neutron star
        "irrep": "A1g",
        "embedding": 1,
        "parity": 0,
        "spin_x2": 1,
        "spin_z_x2": 2,
        "isospin_x2": 3,
        "isospin_z_x2": 10000,
        "momentum": 0,
    }
