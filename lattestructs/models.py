# pylint: disable=C0111, R0903, E1101
"""Lattice structure tables
"""
from django.db import models


class GaugeConfig(models.Model):
    """
    """

    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class HisqGaugeConfig(GaugeConfig):
    """
    """

    mpi = models.FloatField()


class CloverGaugeConfig(GaugeConfig):
    """
    """

    lattice_spacing = models.FloatField()


class Propagator(models.Model):
    """
    """

    id = models.AutoField(primary_key=True)
    gauge_config = models.ForeignKey(GaugeConfig, models.CASCADE)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class HisqPropagator(Propagator):
    """
    """

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class CloverPropagator(Propagator):
    """
    """

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"
