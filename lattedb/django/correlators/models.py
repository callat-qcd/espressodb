from django.db import models
from lattedb.django.base.models import Correlators
from lattedb.django.base.models import StatusBase

# Create your models here.
class MesonTwoPoints(Correlators):
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    propagator0 = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to first propagator",
    )
    propagator1 = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to second propagator",
    )
    sourceoperator = models.ForeignKey(
        "base.stateoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to source interpolating operator",
    )
    sinkoperator = models.ForeignKey(
        "base.stateoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey: Pointer to sink interpolating operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "propagator1", "sourceoperator", "sinkoperator"],
                name="unique_mesontwopoints",
            )
        ]


class MesonTwoPointsSimulationDetail(Correlators, StatusBase):
    mesontwopoints_ptr = models.ForeignKey(
        "correlators.MesonTwoPoints",
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
