from django.db import models
from lattedb.django.base.models import Status

# Create your models here.
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
        "correlator.baryonseq3pt",
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