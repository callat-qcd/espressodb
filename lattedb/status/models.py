from django.db import models

from lattedb.base.models import Base


class Status(Base):
    """ Base table for application
    """
    trajectory = models.PositiveSmallIntegerField(
        null=False,
        help_text="PositiveSmallInt: Monte Carlo trajectory (config number) of object"
    )
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


class Ensemble_Flavor211(Status):
    ensemble = models.ForeignKey(
        "ensemble.Flavor211",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to 2+1+1 flavor ensemble",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trajectory", "ensemble"], name="unique_status_ensemble_flavor211"
            )
        ]


class Propagator_OneToAll(Status):
    """
    """

    propagator = models.ForeignKey(
        "propagator.OneToAll",
        on_delete=models.CASCADE,
        help_text="ForeignKey to one-to-all propagator table",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trajectory", "propagator"], name="unique_status_propagator_onetoall"
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
                fields=["trajectory", "propagator"], name="unique_status_propagator_coherentseq"
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
                fields=["trajectory", "propagator"], name="unique_status_propagator_feynmanhellmann"
            )
        ]


class Correlator_DWFTuning(Status):
    correlator = models.ForeignKey(
        "correlator.dwftuning",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to mres and phi_qq correlation functions",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trajectory", "correlator"], name="unique_status_correlator_dwftuning"
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
                fields=["trajectory", "correlator"], name="unique_status_correlator_meson2pt"
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
                fields=["trajectory", "correlator"], name="unique_status_correlator_baryon4dseq3pt"
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
                fields=["trajectory", "correlator"], name="unique_status_correlator_baryonfh3pt"
            )
        ]
