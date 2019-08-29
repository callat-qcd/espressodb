from typing import Optional

from django.db import models
from django.core.exceptions import ValidationError

from lattedb.base.models import Base

from lattedb.gaugeconfig.models import GaugeConfig


class Ensemble(Base):
    """Implementation of ensemble of configurations table
    """

    configurations = models.ManyToManyField(GaugeConfig)
    label = models.CharField(
        max_length=40,
        null=False,
        blank=False,
        unique=True,
        help_text="(Optional) Char(20): label to identify ensemble for easy searches",
    )

    @property
    def short_tag(self) -> Optional[str]:
        """Returns the tag of the first configuration.
        """
        first = self.configurations.first()  # pylint: disable=E1101
        return first.short_tag if first else None

    def long_tag(self) -> Optional[str]:
        """Returns descriptive long tag of first configuration
        """
        first = self.configurations.first()  # pylint: disable=E1101
        return first.long_tag if first else None

    def check_consistency(self):
        """Checks if all configurations have the same meta info.
        """
        first = self.configurations.first()  # pylint: disable=E1101
        if first:
            for config in self.configurations.all()[1:]:  # pylint: disable=E1101
                if not first.same_ensemble(config):
                    raise ValidationError(
                        f"{config} if different from first config {first}"
                    )
