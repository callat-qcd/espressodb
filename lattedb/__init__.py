# pylint: disable=C0413
"""Easy access to models
"""

from lattedb.interface.init import init

init()

from lattedb.django.gaugeconfigs.models import CloverGaugeConfig
from lattedb.django.gaugeconfigs.models import HisqGaugeConfig
