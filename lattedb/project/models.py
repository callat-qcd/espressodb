from lattedb.base.models import Base


class Data(Base):
    """Abstract base table for data
    """

    class Meta:
        abstract = True


class Project(Base):
    """Abstract base table for projects
    """

    class Meta:
        abstract = True
