from django.db import models
from lattedb.django.base.models import GaugeConfigurations
from lattedb.django.base.models import StatusBase


class HisqGaugeConfigurations(GaugeConfigurations):
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
    nx = models.PositiveSmallIntegerField(
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
        max_digits=6,
        decimal_places=4,
        null=False,
        help_text="Decimal(6,4): Coupling constant",
    )
    naik = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )
    u0 = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(7,6): Tadpole improvement coefficient",
    )
    a_fm = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        null=True,
        help_text="(Optional) Decimal(4,3): Lattice spacing in fermi",
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nx", "nt", "ml", "ms", "mc", "beta", "naik"],
                name="unique_hisqgaugeconfigurations",
            )
        ]


class HisqGaugeConfigurationsSimulationDetail(GaugeConfigurations, StatusBase):
    hisqgaugeconfigurations_ptr = models.ForeignKey(
        "gaugeconfigurations.HisqGaugeConfigurations",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to HISQ ensemble",
    )

    stream = models.CharField(
        max_length=3,
        null=False,
        blank=False,
        help_text="Charfield(3): Stream tag for Monte Carlo",
    )
    num_configurations = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Number of configurations"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hisqgaugeconfigurations_ptr", "stream", "num_configurations"],
                name="unique_hisqgaugeconfigurationssimulationdetail",
            )
        ]


class CloverGaugeConfigurations(GaugeConfigurations):
    """
    """

    lattice_spacing = models.FloatField()
