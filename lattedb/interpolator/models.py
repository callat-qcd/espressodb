from django.db import models

from lattedb.base.models import Base


class Interpolator(Base):
    """ Base table for application
    """


class Hadron4D(Interpolator):
    """
    """

    description = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Description of the interpolating operator",
    )
    interpolatorsmear = models.ForeignKey(
        "interpolatorsmear.InterpolatorSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to operator smearing",
    )
    strangeness = models.PositiveSmallIntegerField(
        null=False,
        help_text="PositiveSmallIntegerField: Strangeness of hadronic operator",
    )
    irrep = models.TextField(
        null=False,
        blank=False,
        help_text="Text: Irreducible representations of O^D_h (octahedral group)",
    )
    embedding = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallIntegerField: k-th embedding of O^D_h irrep.",
    )

    parity = models.SmallIntegerField(
        null=False, help_text="SmallIntegerField: Parity of hadronic operator"
    )
    spin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Text: Total spin times two"
    )

    spin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Text: Spin in z-direction"
    )

    isospin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Text: Total isospin times two"
    )

    isospin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Text: Isospin in z-direction times two"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "interpolatorsmear",
                    "strangeness",
                    "irrep",
                    "embedding",
                    "parity",
                    "spin_x2",
                    "spin_z_x2",
                    "isospin_x2",
                    "isospin_z_x2",
                ],
                name="unique_hadron_hadron4d",
            )
        ]


class Hadron(Interpolator):

    description = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Description of the interpolating operator",
    )
    interpolatorsmear = models.ForeignKey(
        "interpolatorsmear.InterpolatorSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to operator smearing",
    )
    strangeness = models.PositiveSmallIntegerField(
        null=False,
        help_text="PositiveSmallIntegerField: Strangeness of hadronic operator",
    )
    irrep = models.TextField(
        null=False,
        blank=False,
        help_text="Text: Irreducible representations of O^D_h (octahedral group)",
    )
    embedding = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="PositiveSmallIntegerField: k-th embedding of O^D_h irrep.",
    )

    parity = models.SmallIntegerField(
        null=False, help_text="SmallIntegerField: Parity of hadronic operator"
    )
    spin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Text: Total spin times two"
    )

    spin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Text: Spin in z-direction"
    )

    isospin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Text: Total isospin times two"
    )

    isospin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Text: Isospin in z-direction times two"
    )

    momentum = models.SmallIntegerField(
        help_text="SmallInt: Momentum in units of 2 pi / L"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "interpolatorsmear",
                    "strangeness",
                    "irrep",
                    "embedding",
                    "parity",
                    "spin_x2",
                    "spin_z_x2",
                    "isospin_x2",
                    "isospin_z_x2",
                    "momentum",
                ],
                name="unique_hadron_hadron",
            )
        ]
