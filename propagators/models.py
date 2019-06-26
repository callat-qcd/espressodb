from django.db import models

from base.models import Propagator

# Create your models here.


class HisqPropagator(Propagator):
    """
    """
    gaugeconfig = models.ForeignKey('base.GaugeConfig', on_delete=models.CASCADE, help_text="ForeignKey pointing to gauge field.")
    linksmearing = models.ForeignKey('base.LinkSmearing', on_delete=models.CASCADE, help_text="ForeignKey pointing to link smearing")
    mval = models.DecimalField(max_digits=7, decimal_places=6, null=False, help_text="Decimal(7,6): Input valence quark mass")


class CloverPropagator(Propagator):
    """
    """
