from django.db import models
from django.contrib.postgres.fields import JSONField

from lattedb.django.base.models import Base

class Correlator(Base):
    """ Base table for application
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

# Create your models here.
class Meson2pt(Correlator):
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
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
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
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
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
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
