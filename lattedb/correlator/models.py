from django.db import models

from lattedb.base.models import Base

class Correlator(Base):
    """ Base table for application
    """

# Create your models here.admin@ithems.lbl.gov
class DWFTuning(Correlator):
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to first propagator",
    )
    source = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sink5 = models.BooleanField(
        null=False,
        help_text="Boolean: Is the sink on the domain wall?"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator", "source", "sink5"],
                name="unique_correlator_dwftuning",
            )
        ]

class Meson2pt(Correlator):
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to first propagator",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to second propagator",
    )
    source = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sink = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )
    momentum = models.SmallIntegerField(
        help_text="SmallInt: Total momentum in units of 2 pi / L"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "propagator1", "source", "sink", "momentum"],
                name="unique_correlator_meson2pt",
            )
        ]


class Baryon4DSeq3pt(Correlator):
    source = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to source operator",
    )
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        help_text="Foreign Key to current interaction operator",
    )
    seqpropagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to sequential propagator",
    )
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "source",
                    "current",
                    "seqpropagator",
                    "propagator0",
                    "propagator1",
                ],
                name="unique_correlator_baryonseq3pt",
            )
        ]


class BaryonFH3pt(Correlator):
    source = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to source operator",
    )
    fhpropagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to Feynman-Hellmann propagator",
    )
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )
    sink = models.ForeignKey(
        "hadron.Hadron",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to sink operator",
    )
    momentum = models.SmallIntegerField(
        help_text="SmallInt: Sink momentum in units of 2 pi / L"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "source",
                    "fhpropagator",
                    "propagator0",
                    "propagator1",
                    "sink",
                    "momentum",
                ],
                name="unique_correlator_baryonfh3pt",
            )
        ]
