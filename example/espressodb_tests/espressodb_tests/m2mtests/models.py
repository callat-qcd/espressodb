# pylint: disable=C0103
"""Example models to test check consistency methods of the many to many signals
"""
from django.db import models
from espressodb.base.models import Base


class A(Base):
    """Blank table with no columns
    """


class B(Base):
    """First many to many class
    """

    a_set = models.ManyToManyField(A)


class C(Base):
    """First class with two many to many fields
    """

    a_set = models.ManyToManyField(A)
    b_set = models.ManyToManyField(B)
