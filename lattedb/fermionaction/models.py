from django.db import models

from lattedb.base.models import Base


class FermionAction(Base):
    """ Base table for application
    """


class Hisq(FermionAction):
    """
    """

    quark_mass = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input quark mass",
    )
    quark_tag = models.TextField(
        blank=False, null=False, help_text="Text: Type of quark"
    )

    naik = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )
    linksmear = models.ForeignKey(
        "linksmear.LinkSmear",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to additional gauge link smearing outside of Monte Carlo.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quark_mass", "quark_tag", "naik", "linksmear"],
                name="unique_fermionaction_hisq",
            )
        ]


class MobiusDW(FermionAction):
    """
    """

    quark_mass = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input quark mass",
    )
    quark_tag = models.TextField(
        blank=False, null=False, help_text="Text: Type of quark"
    )

    l5 = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Length of 5th dimension"
    )
    m5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): 5th dimensional mass",
    )
    b5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernel parameter [a5 = b5 - c5, alpha5 * a5 = b5 + c5]",
    )
    c5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernal perameter",
    )
    linksmear = models.ForeignKey(
        "linksmear.LinkSmear",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to additional gauge link smearing outside of Monte Carlo.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quark_mass", "quark_tag", "l5", "m5", "b5", "c5", "linksmear"],
                name="unique_fermionaction_mobiusdw",
            )
        ]

    @property
    def alpha5(self) -> float:
        """c5 + b5
        """
        return self.c5 + self.b5
