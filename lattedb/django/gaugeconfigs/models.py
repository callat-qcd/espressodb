from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

from lattedb.django.base.models import GaugeConfig


class HisqGaugeConfig(GaugeConfig):
    """
    """

    long_tag = models.TextField(null=False, blank=True)
    short_tag = models.CharField(max_length=20, null=False, blank=True)
    stream = models.CharField(max_length=5, null=False, blank=False)
    nl = models.PositiveSmallIntegerField(null=False)
    nt = models.PositiveSmallIntegerField(null=False)
    ml = models.DecimalField(max_digits=7, decimal_places=6, null=False)
    ms = models.DecimalField(max_digits=6, decimal_places=5, null=False)
    mc = models.DecimalField(max_digits=5, decimal_places=4, null=False)
    beta = models.DecimalField(max_digits=5, decimal_places=3, null=False)
    a_fm = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    l_fm = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    mpil = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    mpi = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    alpha_s = models.FloatField(null=True)
    directory = models.TextField(null=False, blank=True)
    misc = JSONField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stream", "nl", "nt", "ml", "ms", "mc", "beta"],
                name="unique_hisqgaugeconfigs",
            )
        ]


class CloverGaugeConfig(GaugeConfig):
    """
    """

    lattice_spacing = models.FloatField()
