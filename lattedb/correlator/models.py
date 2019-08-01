from django.db import models
from django.core.exceptions import ValidationError

from lattedb.base.models import Base


class Correlator(Base):
    """ Base table for application
    """


# Create your models here.
class DWFTuning(Correlator):
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to first propagator",
    )
    source = models.ForeignKey(
        "interpolator.Interpolator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sink5 = models.BooleanField(
        null=False, help_text="Boolean: Is the sink on the domain wall?"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator", "source", "sink5"],
                name="unique_correlator_dwftuning",
            )
        ]

    def clean(self):
        """Sets tag of the correlator based on sink5.
        """
        if self.tag is None:
            self.tag = "pseudo_pseudo" if self.sink5 else "midpoint_pseudo"


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
        "interpolator.Interpolator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sink = models.ForeignKey(
        "interpolator.Interpolator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "propagator1", "source", "sink"],
                name="unique_correlator_meson2pt",
            )
        ]

    def clean(self):
        """Sets tag of the correlator based on propagators, the gaugeconfig and source.

        Operators are sorted by their `mval` key.
        """
        p0 = self.propagator0
        p1 = self.propagator1
        if p1 < p0:  # sorted by mval
            self.propagator0 = p1
            self.propagator1 = p0

        if self.tag is None:
            gc0 = self.propagator0.gaugeconfig.specialization  # pylint: disable=E1101
            p0 = self.propagator0.specialization  # pylint: disable=E1101
            gc1 = self.propagator1.gaugeconfig.specialization  # pylint: disable=E1101
            p1 = self.propagator1.specialization  # pylint: disable=E1101

            if gc0 != gc1:
                raise ValidationError(
                    "What are you smoking?"
                    " Propagators not on the same gaugeconfig?!"
                    f"\n{gc0} != {gc1}"
                )

            strangeness = self.source.strangeness  # pylint: disable=E1101
            if abs(strangeness) == 0:  # pylint: disable=E1101
                dtype = "pion"
            elif abs(strangeness) == 1:  # pylint: disable=E1101
                dtype = "kaon"
            elif abs(strangeness) == 2:  # pylint: disable=E1101
                dtype = "etas"
            else:
                raise ValidationError(
                    f"Received strangeness {strangeness} meson."
                    " Don't know how to deal with that..."
                )

            if p1 == p0:
                self.tag = f"{p0.tag}_on_{gc0.tag}_{dtype}"
            else:
                self.tag = f"{p1.tag}{p0.tag}_on_{gc0.tag}_{dtype}"


class Baryon4DSeq3pt(Correlator):
    source = models.ForeignKey(
        "interpolator.Interpolator",
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
        help_text="Foreign Key pointing to sequential propagator (2 spectator quarks + 1 daughter)",
    )
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to daughter quark",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "source",
                    "current",
                    "seqpropagator",
                    "propagator",
                ],
                name="unique_correlator_baryonseq3pt",
            )
        ]


class BaryonFH3pt(Correlator):
    source = models.ForeignKey(
        "interpolator.Interpolator",
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
        "interpolator.Interpolator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to sink operator",
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
                ],
                name="unique_correlator_baryonfh3pt",
            )
        ]
