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
    wave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source spin color space wave function",
    )
    sink5 = models.BooleanField(
        null=False, help_text="Boolean: Is the sink on the domain wall?"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator", "wave", "sink5"],
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
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "propagator1", "sourcewave", "sinkwave"],
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


class Baryon2pt(Correlator):
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
    propagator2 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to third propagator",
    )
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "propagator0",
                    "propagator1",
                    "propagator2",
                    "sourcewave",
                    "sinkwave",
                ],
                name="unique_correlator_baryon2pt",
            )
        ]

    def origin(self):
        return "(%d, %d, %d, %d)" % (
            self.propagator0.specialization.origin_x,
            self.propagator0.specialization.origin_y,
            self.propagator0.specialization.origin_z,
            self.propagator0.specialization.origin_t,
        )

    origin.short_description = "origin (x, y, z, t)"

    @classmethod
    def get_from_ensemble(
        cls,
        ensemble: "Ensemble",
        propagator: str = "propagator0",
        propagator_type: str = "OneToAll",
    ) -> "QuerySet(Baryon2pt)":
        """Returns all correlators which are associated with the ensemble.

        The association is given through the propagator relation.

        **Arguments**
            ensemble: Ensemble
                The ensemble of gaugeconfigs

            propagator: str = "propagator0"
                The propagator of the correlator associated with the gagugeconfig.
                For this correlator, can be one out of
                `[propagator0, propagator1, propagator2]`, but all should be on the same
                gaugeconfig anyway.

            propagator_type: str = "OneToAll"
                The type of the propagator e.g. "OneToAll".
        """
        table_filter = {
            f"{propagator}"
            f"__{propagator_type.lower()}"
            f"__gaugeconfig__in": ensemble.configurations.all()
        }
        return cls.objects.filter(**table_filter)

    @property
    def n_config(self) -> int:
        """The number of the gaugeconfig.
        """
        return self.propagator0.gaugeconfig.config

    @property
    def short_tag(self) -> str:
        """The short tag of the gaugeconfig.
        """
        return self.propagator0.gaugeconfig.short_tag

    @property
    def stream(self) -> str:
        """The stream of the gaugeconfig.
        """
        return self.propagator0.gaugeconfig.stream


class BaryonSeq3pt(Correlator):
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
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
                fields=["sourcewave", "current", "seqpropagator", "propagator"],
                name="unique_correlator_baryonseq3pt",
            )
        ]


class BaryonFH3pt(Correlator):
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to source operator",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to sink operator",
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "sourcewave",
                    "fhpropagator",
                    "propagator0",
                    "propagator1",
                    "sinkwave",
                ],
                name="unique_correlator_baryonfh3pt",
            )
        ]
