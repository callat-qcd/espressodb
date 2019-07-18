from django.db import models

from lattedb.base.models import Base


class Propagator(Base):
    """ Base table for application
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )
    action = models.ForeignKey(
        "action.Action",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to valence lattice action",
    )
    mval = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input valence quark mass",
    )

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Can only compare propagator with other propagator."
                f" Received {other}"
            )
        return self.mval < other.mval

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gaugeconfig", "action", "mval"],
                name="unique_propagator",
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
                    "propagator_ptr_id",  # this has sea and valence action info
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
                    "propagator_ptr_id",
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

    propagator = models.ForeignKey(
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
    momentum = models.SmallIntegerField(
        help_text="SmallInt: Current insertion momentum in units of 2 pi / L"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator_ptr_id", "propagator", "current", "momentum"],
                name="unique_propagator_feynmanhellmann",
            )
        ]
