from django.db import models

from lattedb.base.models import Base


class Hadron(Base):
    """ Base table for application
    """

    description = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Description of the interpolating operator",
    )


class Meson(Hadron):
    """
    """

    hadronsmear = models.ForeignKey(
        "hadronsmear.HadronSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to operator smearing",
    )
    structure = models.TextField(
        null=False, blank=False, help_text="Text: Dirac structure of the operator"
    )
    parity = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        null=False,
        help_text="Decimal(1,0): Parity of hadronic operator",
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

    strangeness = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        null=False,
        help_text="Decimal(1,0): Strangeness of hadronic operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "hadronsmear",
                    "structure",
                    "parity",
                    "spin_x2",
                    "spin_z_x2",
                    "isospin_x2",
                    "isospin_z_x2",
                    "strangeness",
                ],
                name="unique_hadron_meson",
            )
        ]


class Basak(Hadron):
    """
    """

    hadronsmear = models.ForeignKey(
        "hadronsmear.HadronSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to operator smearing",
    )
    irrep = models.TextField(
        null=False,
        blank=False,
        help_text="Text: Irreducible representations of O^D_h (octahedral group)",
    )

    parity = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        null=False,
        help_text="Decimal(1,0): Parity of hadronic operator",
    )
    embedding = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        null=False,
        blank=False,
        help_text="Decimal(1,0): k-th embedding of O^D_h irrep.",
    )

    spin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Text: Total spin times two"
    )

    spin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Text: Spin in z-direction times two"
    )

    isospin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Text: Total isospin times two"
    )

    isospin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Text: Isospin in z-direction times two"
    )

    strangeness = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        null=False,
        help_text="Decimal(1,0): Strangeness of hadronic operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "hadronsmear",
                    "irrep",
                    "parity",
                    "embedding",
                    "spin_x2",
                    "spin_z_x2",
                    "isospin_x2",
                    "isospin_z_x2",
                    "strangeness",
                ],
                name="unique_hadron_basak",
            )
        ]
