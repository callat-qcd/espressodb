from django.db import models

from lattedb.base.models import Base


class FermionAction(Base):
    """ Base table for application
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quark_mass", "quark_tag", "type"], name="unique_fermionaction"
            )
        ]


class Hisq(FermionAction):
    """
    """

    naik = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fermionaction_ptr_id", "naik"], name="unique_fermionaction_hisq"
            )
        ]


class MobiusDW(FermionAction):
    """
    """

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fermionaction_ptr_id", "l5", "m5", "b5", "c5"],
                name="unique_fermionaction_mobiusdw",
            )
        ]
