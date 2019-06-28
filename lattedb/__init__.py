# pylint: disable=C0413
"""Easy access to models
"""

from lattedb.interface.init import init

init()

from lattedb.django.gaugeconfigurations.models import CloverGaugeConfig
from lattedb.django.gaugeconfigurations.models import HisqGaugeConfig
