# pylint: disable=C0103
"""Example models for tests
"""
from django.db import models
from espressodb.base.models import Base


class CA(Base):
    """Blank table with no columns
    """

    def __str__(self):
        return f"A(pk={self.pk})"

    def __repr__(self):
        return str(self)


class CB(Base):
    """First many to many class
    """

    def __str__(self):
        return f"B(pk={self.pk})"

    def __repr__(self):
        return str(self)
