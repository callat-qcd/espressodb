from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

from lattedb.django.base.models import GaugeConfig


class HisqGaugeConfig(GaugeConfig):
    """
    """

    long_tag = models.TextField(
        null=False,
        blank=True,
        help_text="(Optional) Text: Full name for ensemble (e.g. 'l1648f211b580m013m065m838')",
    )
    short_tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): Short name for ensemble (e.g. 'a15m310')",
    )
    nl = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Spatial length in lattice units"
    )
    nt = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Temporal length in lattice units"
    )
    ml = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Input light quark mass",
    )
    ms = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        null=False,
        help_text="Decimal(6,5): Input strange quark mass",
    )
    mc = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        null=False,
        help_text="Decimal(5,4): Input charm quark mass",
    )
    beta = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=False,
        help_text="Decimal(5,3): Coupling constant",
    )
    a_fm = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        null=True,
        help_text="(Optional) Decimal(4,3): Lattice spaing in fermi",
    )
    l_fm = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        help_text="(Optional) Decimal(5,3): Spatial length in fermi",
    )
    mpil = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        help_text="(Optional) Decimal(5,3): Spatial length in mpiL",
    )
    mpi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        help_text="(Optional) Decimal(5,2): Pion mass in MeV",
    )
    alpha_s = models.FloatField(
        null=True, help_text="(Optional) Float: Running coupling"
    )
    directory = models.TextField(
        null=False,
        blank=True,
        help_text="(Optional) Text: Directory path to gauge field",
    )
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

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
