from django.db import models

from lattedb.base.models import Base


class Propagator(Base):
    """ Base table for application
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gaugeconfig", "fermionaction", "type"], name="unique_propagator"
            )
        ]


class OneToAll(Propagator):
    """
    """

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
                    "propagator_ptr_id",  # this has sea and valence fermionaction info
                    "origin_x",
                    "origin_y",
                    "origin_z",
                    "origin_t",
                ],
                name="unique_propagator_onetoall",
            )
        ]


class CoherentSeq(Propagator):
    """
    """

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
    sink = models.ForeignKey(
        "interpolator.Interpolator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )
    sinksep = models.SmallIntegerField(help_text="SmallInt: Source-sink separation time")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "propagator_ptr_id",
                    "propagator0",
                    "propagator1",
                    "groupsize",
                    "groupindex",
                    "sink",
                    "sinksep",
                ],
                name="unique_propagator_coherentseq",
            )
        ]


class FeynmanHellmann(Propagator):
    """
    """

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator_ptr_id", "propagator", "current"],
                name="unique_propagator_feynmanhellmann",
            )
        ]
