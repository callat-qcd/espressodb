from django.test import TestCase

from lattedb.correlator.models import Meson2pt
from lattedb.gaugeconfig.models import Hisq

# Create your tests here.


class Meson2ptTestCase(TestCase):

    parameters = {
        "gagugeconfig": {
            "short_tag": "a15m310",
            "stream": "a",
            "nconfig": 500,
            "nx": 48,
            "nt": 64,
            "ml": 1.0,
            "ms": 2.0,
            "mc": 3.0,
            "beta": 4.0,
            "naik": 5.0,
            "u0": 6.0,
            "a_fm": 7.0,
            "l_fm": 8.0,
            "mpil": 16.0,
            "mpi": 2.0,
        },
        "propagator": {
            "mval": 10,
            "origin_x": 1,
            "origin_y": 2,
            "origin_z": 3,
            "origin_t": 10,
            "l5": 1,
            "m5": 2,
            "alpha5": 5,
            "a5": 10,
            "b5": 2,
            "c5": 5,
        },
        "source": {},
        "sink": {},
        "hadron": {
            "structure": "$\gamma_5$",
            "parity": 1,
            "spin": "up",
            "spin_z": "down",
            "isospin": "bla",
            "isospin_z": "100k",
            "strangeness": 1,
        },
        "hadronsmear": {"radius": 10, "step": 2},
        "gaugesmear": {"flowtime": 1.0, "flowstep": 100},
        "meson2pt": {"momentum": 100},
    }

    def test_get_or_create_from_parameters(self):
        """
        """
        parameters = {}
        for pars in self.parameters.values():
            parameters.update(pars)

        instances = Meson2pt.get_or_create_from_parameters(
            parameters,
            tree={
                "propagator0": (
                    "Hisq",
                    {"gaugeconfig": "Hisq", "gaugesmear": "Unsmeared"},
                ),
                "propagator1": (
                    "MobiusDWF",
                    {"gaugeconfig": "Hisq", "gaugesmear": "WilsonFlow"},
                ),
                "source": ("Meson", {"hadronsmear": "Gaussian"}),
                "sink": ("Meson", {"hadronsmear": "Unsmeared"}),
            },
        )
