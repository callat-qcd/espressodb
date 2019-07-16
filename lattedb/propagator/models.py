from django.db import models

from lattedb.base.models import Base


class Propagator(Base):
    """ Base table for application
    """


class Hisq(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to gauge field",
    )
    gaugesmear = models.ForeignKey(
        "gaugesmear.GaugeSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to gauge link smearing",
    )
    mval = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input valence quark mass",
    )
    naik = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )

    origin_x = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: x-coordinate origin location of the propagator",
    )
    origin_y = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: y-coordinate origin location of the propagator",
    )
    origin_z = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: z-coordinate origin location of the propagator",
    )
    origin_t = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: t-coordinate origin location of the propagator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "gaugesmear",
                    "mval",
                    "naik",
                    "origin_x",
                    "origin_y",
                    "origin_z",
                    "origin_t",
                ],
                name="unique_propagator_hisq",
            )
        ]


class MobiusDWF(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )
    gaugesmear = models.ForeignKey(
        "gaugesmear.GaugeSmear",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge link smearing",
    )
    mval = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input valence quark mass",
    )
    l5 = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Length of 5th dimension"
    )
    m5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): 5th dimensional mass",
    )
    alpha5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius coefficient [D_mobius(M5) = alpha5 * D_Shamir(M5)]",
    )
    a5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernel parameter [D_mobius = alpha5 * a5 * D_Wilson / (2 + a5 * D_Wilson)]",
    )
    b5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernel parameter [a5 = b5 - c5, alpha5 * a5 = b5 + c5]",
    )
    c5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernal perameter",
    )
    origin_x = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: x-coordinate origin location of the propagator",
    )
    origin_y = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: y-coordinate origin location of the propagator",
    )
    origin_z = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: z-coordinate origin location of the propagator",
    )
    origin_t = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallInt: t-coordinate origin location of the propagator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "gaugesmear",
                    "mval",
                    "l5",
                    "m5",
                    "alpha5",
                    "a5",
                    "b5",
                    "c5",
                    "origin_x",
                    "origin_y",
                    "origin_z",
                    "origin_t",
                ],
                name="unique_propagator_mobiusdwf",
            )
        ]


class CoherentSeq(Propagator):
    """
    """

    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey that link to a coherent propagator",
    )
    groupsize = models.PositiveSmallIntegerField(
        help_text="PositiveSmallint: Total number of propagators sharing a coherent sink"
    )
    groupindex = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: A group index indicating which coherent sink group the propagator belongs to"
    )
    sink = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )
    sinksep = models.SmallIntegerField(
        help_text="SmallInt: Source-sink separation time"
    )
    momentum = models.SmallIntegerField(
        help_text="SmallInt: Sink momentum in units of 2 pi / L"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "propagator",
                    "groupsize",
                    "groupindex",
                    "sink",
                    "sinksep",
                    "momentum",
                ],
                name="unique_propagator_coherentseq",
            )
        ]


class FeynmanHellmann(Propagator):
    """
    """

    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking source side propagator",
    )
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking current insertion operator",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking sink side propagator",
    )
    momentum = models.SmallIntegerField(
        help_text="SmallInt: Current insertion momentum in units of 2 pi / L"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "current", "propagator1", "momentum"],
                name="unique_propagator_feynmanhellmann",
            )
        ]
