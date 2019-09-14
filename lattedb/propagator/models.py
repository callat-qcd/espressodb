from django.db import models

from lattedb.base.models import Base


class Propagator(Base):
    """ Base table for application
    """


class OneToAll(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to specific gauge configuration inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to valence lattice fermion action",
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
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to source quark smearing",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to sink quark smearing",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "origin_x",
                    "origin_y",
                    "origin_z",
                    "origin_t",
                    "sourcesmear",
                    "sinksmear",
                ],
                name="unique_propagator_onetoall",
            )
        ]


class CoherentSeq(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to specific gauge configuration inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to valence lattice fermion action",
    )
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey that link to a coherent propagator (spectator 0)",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey that link to a coherent propagator (spectator 1)",
    )
    groupsize = models.PositiveSmallIntegerField(
        help_text="PositiveSmallint: Total number of propagators sharing a coherent sink"
    )
    groupindex = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: A group index indicating which coherent sink group the propagator belongs to"
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )
    sinksep = models.SmallIntegerField(help_text="SmallInt: Source-sink separation time")
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to source quark smearing",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to sink quark smearing",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "propagator0",
                    "propagator1",
                    "groupsize",
                    "groupindex",
                    "sourcesmear",
                    "sinksmear",
                    "sinkwave",
                    "sinksep",
                ],
                name="unique_propagator_coherentseq",
            )
        ]


class FeynmanHellmann(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to specific gauge configuration inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to valence lattice fermion action",
    )
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking RHS propagator",
    )
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey linking momentum space current insertion",
    )
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to source quark smearing",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to sink quark smearing",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "propagator",
                    "current",
                    "sourcesmear",
                    "sinksmear",
                ],
                name="unique_propagator_feynmanhellmann",
            )
        ]
