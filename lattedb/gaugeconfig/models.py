from django.db import models

from lattedb.base.models import Base


class GaugeConfig(Base):
    """ Base table for application
    """


class Hisq(GaugeConfig):
    """
    """

    short_tag = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Short name for ensemble (e.g. 'a15m310')",
    )
    stream = models.TextField(
        null=False, blank=False, help_text="Text: Stream tag for Monte Carlo"
    )
    nconfig = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Number of configurations"
    )
    nx = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Spatial length in lattice units"
    )
    nt = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Temporal length in lattice units"
    )
    ml = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input light quark mass",
    )
    ms = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input strange quark mass",
    )
    mc = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input charm quark mass",
    )
    beta = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coupling constant",
    )
    naik = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )
    u0 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="Decimal(10,6): Tadpole improvement coefficient",
    )
    a_fm = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Lattice spacing in fermi",
    )
    l_fm = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Spatial length in fermi",
    )
    mpil = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Spatial length in mpiL",
    )
    mpi = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Pion mass in MeV",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "stream",
                    "nconfig",
                    "nx",
                    "nt",
                    "ml",
                    "ms",
                    "mc",
                    "beta",
                    "naik",
                    "u0",
                ],
                name="unique_gaugeconfig_hisq",
            )
        ]
