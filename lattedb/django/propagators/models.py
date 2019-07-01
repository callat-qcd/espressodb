from django.db import models

from lattedb.django.base.models import Propagators
from lattedb.django.base.models import StatusBase

# Create your models here.


class HisqPropagators(Propagators):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )

    gaugeconfiguration = models.ForeignKey(
        "base.GaugeConfigurations",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )
    linksmearing = models.ForeignKey(
        "base.LinkSmearings",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to link smearing",
    )
    mval = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Input valence quark mass",
    )
    naik = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gaugeconfiguration", "linksmearing", "mval", "naik"],
                name="unique_hisqpropagators",
            )
        ]


class HisqPropagatorsSimulationDetail(Propagators, StatusBase):
    """
    """

    hisqpropagators_ptr = models.ForeignKey(
        "propagators.HisqPropagators",
        on_delete=models.CASCADE,
        help_text="ForeignKey to HISQ propagator table",
    )

    origin = models.TextField(
        null=False, blank=False, help_text="Text: Origin location of the propagator"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hisqpropagators_ptr", "origin"],
                name="unique_hisqpropagators_simulationparams",
            )
        ]


class MobiusPropagators(Propagators):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    gaugeconfiguration = models.ForeignKey(
        "base.GaugeConfigurations",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )
    linksmearing = models.ForeignKey(
        "base.LinkSmearings",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to link smearing",
    )
    mval = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Input valence quark mass",
    )
    l5 = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Length of 5th dimension"
    )
    m5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): 5th dimensional mass",
    )
    alpha5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius coefficient [D_mobius(M5) = alpha5 * D_Shamir(M5)]",
    )
    a5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius kernel parameter [D_mobius = alpha5 * a5 * D_Wilson / (2 + a5 * D_Wilson)]",
    )
    b5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius kernel parameter [a5 = b5 - c5, alpha5 * a5 = b5 + c5]",
    )
    c5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius kernal perameter",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfiguration",
                    "linksmearing",
                    "mval",
                    "l5",
                    "m5",
                    "alpha5",
                    "a5",
                    "b5",
                    "c5",
                ],
                name="unique_mobiuspropagators",
            )
        ]


class MobiusPropagatorsSimulationDetail(Propagators, StatusBase):
    """
    """

    mobiuspropagators_ptr = models.ForeignKey(
        "propagators.MobiusPropagators",
        on_delete=models.CASCADE,
        help_text="ForeignKey to HISQ propagator table",
    )
    origin = models.TextField(
        null=False, blank=False, help_text="Text: Origin location of the propagator"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mobiuspropagators_ptr", "origin"],
                name="unique_mobiuspropagatorssimulationdetail",
            )
        ]


class CoherentSequentialPropagators(Propagators):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    listofpropagators = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name='+',
        help_text="ForeignKey that link to a list of coherent propagators",
    )
    groupsize = models.PositiveSmallIntegerField(
        help_text="PositiveSmallint: Total number of propagators"
    )
    groupindex = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: A group index indicating which coherent sink group the propagator belongs to"
    )
    sinkoperator = models.ForeignKey(
        "base.stateoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )
    sinkseparationtime = models.SmallIntegerField(
        help_text="SmallInt: Source-sink separation time"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["listofpropagators", "groupsize", "groupindex", "sinkoperator", "sinkseparationtime"],
                name="unique_coherentsequentialpropagators",
            )
        ]

class CoherentSequentialPropagatorsSimulationDetail(Propagators, StatusBase):
    """
    """

    coherentsequentialpropagators_ptr = models.ForeignKey(
        "propagators.CoherentSequentialPropagators",
        on_delete=models.CASCADE,
        help_text="ForeignKey to coherent sequential propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["coherentsequentialpropagators_ptr"],
                name="unique_coherentsequentialpropagatorssimulationdetail",
            )
        ]

class FeynmanHellmannPropagators(Propagators):
    """
    """
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    sourcepropagator = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking source side propagator"
    )
    currentoperator = models.ForeignKey(
        "base.interactionoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking current insertion operator"
    )
    sinkpropagator = models.ForeignKey(
        "base.Propagators",
        on_delete = models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking sink side propagator"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sourcepropagator", "currentoperator", "sinkpropagator"],
                name="unique_feynmanhellmannpropagators"
            )
        ]

class FeynmanHellmannPropagatorsSimulationDetail(Propagators, StatusBase):
    """
    """

    feynmanhellmannpropagators_ptr = models.ForeignKey(
        "propagators.FeynmanHellmannPropagators",
        on_delete=models.CASCADE,
        help_text="ForeignKey to Feynman-Hellmann propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["feynmanhellmannpropagators_ptr"],
                name="unique_feynmanhellmannpropagatorssimulationdetail",
            )
        ]