from django.db import models
from django.contrib.postgres.fields import JSONField

from lattedb.base.models import Base


class Status(Base):
    """ Base table for application
    """

    home = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Computing facility where the object resides at",
    )
    runscript = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Path to, or content of run script",
    )
    directory = models.TextField(
        null=True, blank=True, help_text="(Optional) Text: Directory path to result"
    )
    hdf5path = models.TextField(
        null=True, blank=True, help_text="(Optional) Text: Folder path in hdf5 file"
    )
    size = models.IntegerField(null=True, help_text="(Optional) Int: file size")
    statusencoder = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Encode categorical status labels with values between 0 and n_classes-1"
    )

    class Meta:
        abstract = True


class GaugeConfig_Hisq(Status):
    gaugeconfig = models.ForeignKey(
        "gaugeconfig.Hisq",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to HISQ ensemble",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gaugeconfig"], name="unique_status_gaugeconfig_hisq"
            )
        ]


class Propagator_Hisq(Status):
    """
    """

    propagator = models.ForeignKey(
        "propagator.Hisq",
        on_delete=models.CASCADE,
        help_text="ForeignKey to HISQ propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator"], name="unique_status_propagator_hisq"
            )
        ]


class Propagator_MobiusDWF(Status):
    """
    """

    propagator = models.ForeignKey(
        "propagator.MobiusDWF",
        on_delete=models.CASCADE,
        help_text="ForeignKey to HISQ propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator"], name="unique_status_propagator_mobiusdwf"
            )
        ]


class Propagator_CoherentSeq(Status):
    """
    """

    propagator = models.ForeignKey(
        "propagator.CoherentSeq",
        on_delete=models.CASCADE,
        help_text="ForeignKey to coherent sequential propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator"], name="unique_status_propagator_coherentseq"
            )
        ]


class Propagator_FeynmanHellmann(Status):
    """
    """

    propagator = models.ForeignKey(
        "propagator.FeynmanHellmann",
        on_delete=models.CASCADE,
        help_text="ForeignKey to Feynman-Hellmann propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator"], name="unique_status_propagator_feynmanhellmann"
            )
        ]


class Correlator_Meson2pt(Status):
    correlator = models.ForeignKey(
        "correlator.meson2pt",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to meson two point correlation function",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["correlator"], name="unique_status_correlator_meson2pt"
            )
        ]


class Correlator_Baryon4DSeq3pt(Status):
    correlator = models.ForeignKey(
        "correlator.baryon4dseq3pt",
        on_delete=models.CASCADE,
        help_text="Foreign Key to a sequential three point correlation function",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["correlator"], name="unique_status_correlator_baryon4dseq3pt"
            )
        ]


class Correlator_BaryonFH3pt(Status):
    correlator = models.ForeignKey(
        "correlator.BaryonFH3pt",
        on_delete=models.CASCADE,
        help_text="Foreign Key to a Feynman-Hellmann three point correlation function",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["correlator"], name="unique_status_correlator_baryonfh3pt"
            )
        ]
