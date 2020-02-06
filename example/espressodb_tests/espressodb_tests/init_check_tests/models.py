"""Models of init_check_tests
"""

# Note: if you want your models to use espressodb features, they must inherit from Base

from django.db import models
from espressodb.base.models import Base


class AInit(Base):
    """Simple class used in tests
    """

    i = models.IntegerField()
