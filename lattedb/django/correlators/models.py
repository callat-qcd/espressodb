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


class BaryonSequentialThreePoints(Correlators):
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    sourceoperator = models.ForeignKey(
        "base.stateoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to source operator",
    )
    interactionoperator = models.ForeignKey(
        "base.interactionoperators",
        on_delete=models.CASCADE,
        help_text="Foreign Key to current interaction operator"
    )
    sequentialpropagator = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to sequential propagator",
    )
    spectatorpropagator0 = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )
    spectatorpropagator1 = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "sourceoperator",
                    "interactionoperator",
                    "sequentialpropagator",
                    "spectatorpropagator0",
                    "spectatorpropagator1",
                ],
                name="unique_baryonsequentialthreepoints",
            )
        ]

class BaryonSequentialThreePointsSimulationDetail(Correlators, StatusBase):
    baryonsequentialthreepoints_ptr = models.ForeignKey(
        "correlators.BaryonSequentialThreePoints",
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


class BaryonFeynmanHellmannThreePoints(Correlators):
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    sourceoperator = models.ForeignKey(
        "base.stateoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to source operator",
    )
    feynmanhellmannpropagator = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to Feynman-Hellmann propagator"
    )
    spectatorpropagator0 = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )
    spectatorpropagator1 = models.ForeignKey(
        "base.Propagators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to spectator propagator",
    )
    sinkoperator = models.ForeignKey(
        "base.stateoperators",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Foreign Key pointing to sink operator",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "sourceoperator",
                    "feynmanhellmannpropagator",
                    "spectatorpropagator0",
                    "spectatorpropagator1",
                    "sinkoperator"
                ],
                name="unique_baryonfeynmanhellmannthreepoints",
            )
        ]


class BaryonFeynmanHellmannThreePointsSimulationDetail(Correlators, StatusBase):
    baryonfeynmanhellmannthreepoints_ptr = models.ForeignKey(
        "correlators.BaryonFeynmanHellmannThreePoints",
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