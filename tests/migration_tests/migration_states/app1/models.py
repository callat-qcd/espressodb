"""This apps models migrations and database are all fine.
"""

from django.db import models
from espressodb.base.models import Base


class A1(Base):
    i = models.IntegerField()
