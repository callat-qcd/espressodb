from django.db import models

# Create your models here.

from base.models import GaugeConfig


class HisqGaugeConfig(GaugeConfig):
    """
    """

    short_tag = models.TextField()
    long_tag = models.TextField()
    stream = models.TextField(null=False)
    mpi = models.FloatField()


class CloverGaugeConfig(GaugeConfig):
    """
    """

    lattice_spacing = models.FloatField()
