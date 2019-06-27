from django.db import models
from lattedb.django.base.models import Correlators

# Create your models here.
class MesonTwoPoints(Correlators):
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text='(Optional) Char(20): User defined tag for easy searches'
    )
    propagator0 = models.OneToOneField(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="OneToOneField: Pointer to first propagator"
    )
    propagator1 = models.OneToOneField(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="OneToOneField: Pointer to second propagator"
    )
    sourceoperator = models.OneToOneField(
        "base.interpolatingoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="OneToOneField: Pointer to source interpolating operator"
    )
    sourcesmearing = models.OneToOneField(
        "base.operatorsmearings",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="OneToOneField: Pointer to source operator smearing"
    )
    sinkoperator = models.OneToOneField(
        "base.interpolatingoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="OneToOneField: Pointer to sink interpolating operator"
    )