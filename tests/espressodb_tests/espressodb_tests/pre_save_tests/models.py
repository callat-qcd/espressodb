"""Models of pre_save_test
"""

from django.db import models
from espressodb.base.models import Base

from django.core.validators import MinLengthValidator

VERSION = "v1.1.0"


def get_version_number() -> str:
    """Mocks returning the version string
    """
    return VERSION


class MandatoryTagTable(Base):
    """Blank table to check pre save
    """

    tag = models.CharField(  # Overriding the default tag field to be mandatory
        max_length=200, help_text="User defined tag for easy searches",
    )

    def pre_save(self):
        """Sets the tag using ``get_version_number()``.
        """
        self.tag = get_version_number()

    def check_consistency(self):
        """Checks if tag field is not empty
        """
        if not self.tag:
            raise ValueError("You must specify the tag to save this model.")


class OptionalTagTable(Base):
    """Blank table to check pre save
    """

    def pre_save(self):
        """Sets the tag using ``get_version_number()``.
        """
        self.tag = get_version_number()
