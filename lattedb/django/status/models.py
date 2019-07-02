from django.db import models
from django.contrib.postgres.fields import JSONField

from lattedb.django.base.models import Base

class Status(Base):
    """ Base table for application
    """
    home = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): Computing facility where the object resides at",
    )
    runscript = models.TextField(
        null=False,
        blank=True,
        help_text="(Optional) Text: Path to, or content of run script",
    )
    directory = models.TextField(
        null=False, blank=True, help_text="(Optional) Text: Path to result"
    )
    size = models.IntegerField(null=True, help_text="(Optional) Int: file size")
    statusencoder = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Encode categorical status labels with values between 0 and n_classes-1"
    )

    class Meta:
        abstract = True

class HisqGaugeConfigurationsSimulationDetail(Status):
    hisqgaugeconfigurations_ptr = models.ForeignKey(
        "gaugeconfig.Hisq",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to HISQ ensemble",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hisqgaugeconfigurations_ptr"],
                name="unique_hisqgaugeconfigurationssimulationdetail",
            )
        ]


class HisqPropagatorsSimulationDetail(Status):
    """
    """

    hisqpropagators_ptr = models.ForeignKey(
        "propagator.Hisq",
        on_delete=models.CASCADE,
        help_text="ForeignKey to HISQ propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hisqpropagators_ptr"],
                name="unique_hisqpropagators_simulationparams",
            )
        ]

class MobiusPropagatorsSimulationDetail(Status):
    """
    """

    mobiuspropagators_ptr = models.ForeignKey(
        "propagator.MobiusDWF",
        on_delete=models.CASCADE,
        help_text="ForeignKey to HISQ propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mobiuspropagators_ptr"],
                name="unique_mobiuspropagatorssimulationdetail",
            )
        ]

class CoherentSequentialPropagatorsSimulationDetail(Status):
    """
    """

    coherentsequentialpropagators_ptr = models.ForeignKey(
        "propagator.CoherentSeq",
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

class FeynmanHellmannPropagatorsSimulationDetail(Status):
    """
    """

    feynmanhellmannpropagators_ptr = models.ForeignKey(
        "propagator.FeynmanHellmann",
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

class MesonTwoPointsSimulationDetail(Status):
    mesontwopoints_ptr = models.ForeignKey(
        "correlator.meson2pt",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to meson two point correlation function",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mesontwopoints_ptr"],
                name="unique_mesontwopointssimulationdetail",
            )
        ]

class BaryonSequentialThreePointsSimulationDetail(Status):
    baryonsequentialthreepoints_ptr = models.ForeignKey(
        "correlator.baryon2dseq3pt",
        on_delete=models.CASCADE,
        help_text="Foreign Key to a sequential three point correlation function"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["baryonsequentialthreepoints_ptr"],
                name="unique_baryonsequentialthreepointssimulationdetail",
            )
        ]

class BaryonFeynmanHellmannThreePointsSimulationDetail(Status):
    baryonfeynmanhellmannthreepoints_ptr = models.ForeignKey(
        "correlator.BaryonFH3pt",
        on_delete=models.CASCADE,
        help_text="Foreign Key to a Feynman-Hellmann three point correlation function"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["baryonfeynmanhellmannthreepoints_ptr"],
                name="unique_baryonfeynmanhellmannthreepointssimulationdetail",
            )
        ]