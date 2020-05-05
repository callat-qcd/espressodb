# pylint: disable=C0111, R0903, E1101
"""This module provides the :class:`Base` class which is an abstract model basis
providing default interfaces for :mod:`espressodb`.
"""
from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional
from typing import Any

import logging

from django.db import models
from django.db import connection
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.fields import Field
from django.urls import reverse, Resolver404
from django.apps.config import AppConfig

from django_pandas.managers import DataFrameManager

from espressodb.base.utilities.apps import APPS_TO_SLUG

LOGGER = logging.getLogger("base")


class Base(models.Model):
    """The base class for the espressodb module.

    This class provides api for auto rendering pages and recursive insertions.
    """

    # Run consistency checks on save and m2m update.
    run_checks: bool = True
    # Run custom pre save actions on model before inserting.
    run_pre_save: bool = True

    #: Primary key for the base class
    id = models.AutoField(primary_key=True, help_text="Primary key for Base class.")
    #: Date the class was last modified
    last_modified = models.DateTimeField(
        auto_now=True, help_text="Date the class was last modified"
    )
    #: User who updated this object. Set on save by connection to database.
    #: Anonymous if not found.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="User who updated this object. Set on save by connection to database."
        " Anonymous if not found.",
    )
    #: User defined tag for easy searches
    tag = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="User defined tag for easy searches",
    )

    @classmethod
    def get_slug(cls) -> str:
        """Returns import path as slug name"""
        return slugify(cls.__name__)

    objects = DataFrameManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Default init but adds specialization attributes (which do not clash) to self

        The specialization is a child instance of this class which has an id in the
        respective child table.

        The specialization attributes are attributes present in the child but not in the
        current instance.
        """

        super().__init__(*args, **kwargs)
        self._specialization = None

        self._specialized_keys = []
        if self.specialization != self:
            for field in self.specialization.get_open_fields():
                if field.name not in dir(self):
                    self._specialized_keys.append(field.name)
                    setattr(self, field.name, getattr(self.specialization, field.name))

    @property
    def type(self) -> "Base":
        """Returns the table type
        """
        return self.specialization.__class__.__name__

    @classmethod
    def get_app(cls) -> AppConfig:
        """Returns the name of the current moule app
        """
        return cls._meta.app_config

    @classmethod
    def get_app_name(cls) -> str:
        """Returns the name of the current moule app
        """
        return cls.get_app().verbose_name

    @classmethod
    def get_app_doc_url(cls) -> Optional[str]:
        """Returns the url tp the doc page of the app.

        Returns:
            Url if look up exist else None.
        """
        app_slug = APPS_TO_SLUG.get(cls.get_app())
        try:
            url = reverse("documentation:details", args=[app_slug])
        except Resolver404:
            url = None
        return url

    @classmethod
    def get_doc_url(cls) -> Optional[str]:
        """Returns the url to the doc page.

        Returns:
            Url if look up exist else None.
        """
        app_url = cls.get_app_doc_url()
        return f"{app_url}#{cls.get_slug()}" if app_url is not None else None

    def __setattr__(self, key, value):
        """Tries to set the attribute in specialization if it is a specialized attribute
        and else sets it in parent class.
        """
        if hasattr(self, "_specialized_keys") and key in self._specialized_keys:
            setattr(self.specialization, key, value)
        super().__setattr__(key, value)

    def check_consistency(self):
        """Method is called before save.

        Raise errors here if the model must fulfill checks.
        """

    def pre_save(self):
        """Method is called before save and before check consistency.

        This method can be used to overwrite custom column values.
        It has access to all information present at the ``.save()`` call.
        """

    def check_m2m_consistency(
        self, instances: List["Base"], column: Optional[str] = None
    ):
        """Method is called before adding to a many to many set.

        Raise errors here if the adding must fulfill checks.
        """

    @classmethod
    def get_open_fields(cls) -> List[Field]:
        """Returns list of fields for class which are editable and non-ForeignKeys.
        """
        fields = []
        for field in cls._meta.get_fields():  # pylint: disable=W0212
            if not (
                field.name in ["id", "user"]
                or not field.editable
                or field.name.endswith("_ptr")
            ):
                fields.append(field)
        return fields

    @classmethod
    def get_label(cls) -> str:
        """Returns descriptive string about class
        """
        base = f"[{cls.mro()[1].__name__}]" if cls != Base else ""
        return f"{cls.__name__}{base}"

    def __str__(self) -> str:
        """Verbose description of instance name, parent and column values.
        """
        if self == self.specialization:
            kwargs = {
                field.name: getattr(self, field.name)
                for field in self.get_open_fields()
                if not isinstance(field, models.ForeignKey)
                and not isinstance(field, models.ManyToManyField)
                and getattr(self, field.name) is not None
            }
            base = (
                f"[{self.__class__.mro()[1].__name__}]"
                if type(self) != Base  # pylint: disable=C0123
                else ""
            )
            info = ", ".join([f"{key}={val}" for key, val in kwargs.items()])
            info_str = f"({info})" if info else ""
            out = f"{self.__class__.__name__}{base}{info_str}"
        else:
            out = self.specialization.__str__()
        return out

    def save(  # pylint: disable=W0221
        self, *args, save_instance_only: bool = False, **kwargs,
    ) -> "Base":  # pylint: disable=W0221
        """Overwrites user with login info if not specified and runs consistency checks.

        Arguments:
            save_instance_only:
                If true, only saves columns of the instance and not associated
                specialized columns.

        Note:
            The keyword ``save_instance_only`` and ``check_consistency`` is not present
            in standard Django.
        """
        if not self.user:
            username = settings.DB_CONFIG.get("USER", None)
            if username:
                self.user, _ = User.objects.get_or_create(username=username)
            else:
                self.user, _ = User.objects.get_or_create(username="anonymous")

        if self != self.specialization and not save_instance_only:
            self.specialization.save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

        return self

    @property
    def specialization(self) -> "Base":
        """Returns the specialization of the instance (children with the same id).

        If the class has no children which match the id, this will be the same object.
        """
        if self._specialization is None:
            self._specialization = self.get_specialization()
        return self._specialization

    def get_specialization(self) -> "Base":
        """Queries the dependency tree and returns the most specialized instance of the
        table.
        """
        instance = self
        for cls in self.__class__.__subclasses__():
            match = cls.objects.filter(id=self.id).first()
            if match:  # use that the id is share among other subclasses.
                instance = match.get_specialization()
                break

        return instance

    @classmethod
    def _get_child_by_name(cls, class_name=str) -> "Base":
        """Compares name of cls and all subclasses to ``class_name`` and returns match

        Arguments:
            class_name: The name to match.

        Raises:
            KeyError: In case no or more then one class matches the name.
        """
        class_family = [cls] + cls.__subclasses__()
        matched_cls = [
            el for el in class_family if el.__name__.split(".")[-1] == class_name
        ]
        if len(matched_cls) != 1:
            raise KeyError(
                f"Could not find specialization {class_name}"
                + f" for base class {cls}."
                + "\nPossible options:\n\t"
                + "\n\t".join([el.__name__.split(".")[-1] for el in class_family])
            )
        else:
            expected_cls = matched_cls[0]

        return expected_cls

    @classmethod
    def get_sub_info(
        cls, root_key: str, tree: Dict[str, Any]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Extracts the class name and sub tree for a given tree and key

        Arguments:
            root_key:
                The key to look up in the dictionary

            tree:
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes

        Raises:
            TypeError: If the values of the dictionary are not of type string or Tuple
            KeyError: If the key was not found in the dictionary
        """
        sub_tree = {}
        for key, val in tree.items():
            branches = key.split(".")
            root = branches[0]
            if root == root_key:
                if len(branches) > 1:
                    sub_tree[".".join(branches[1:])] = val

        return sub_tree

    @classmethod
    def get_recursive_columns(
        cls, tree: Optional[Dict[str, Any]] = None, _class_name: Optional[str] = None
    ) -> Tuple[Dict[str, List[str]]]:
        """Recursively parses table including foreign keys to extract all column names.

        Arguments:
            tree:
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes
            _class_name:
                This key is used internaly to identified the specialization of the base
                object.
        """
        tree = tree or {}

        specialization = cls._get_child_by_name(_class_name) if _class_name else cls

        columns = {}
        for field in specialization.get_open_fields():

            if isinstance(field, models.ForeignKey):

                sub_class_name = tree.get(field.name, None)
                if sub_class_name is not None:
                    sub_tree = specialization.get_sub_info(field.name, tree)
                    sub_cols = field.related_model.get_recursive_columns(
                        tree=sub_tree, _class_name=sub_class_name
                    )
                    for key, val in sub_cols.items():
                        columns.setdefault(key, []).extend(
                            [f"{specialization.__name__}.{col}" for col in val]
                        )

            else:
                columns.setdefault(field.name, []).append(specialization.__name__)

        return columns

    @classmethod
    def _get_or_create_fk(  # pylint: disable=R0913
        cls,
        field: models.ForeignKey,
        parameters: Dict[str, Any],
        tree: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        _recursion_level: int = 0,
    ) -> Tuple["Base", bool]:
        """Recursively iterates ForeignKey field and tries to construc the foreign keys
        from parameters and parse tree using `get_or_create_from_parameters`.

        Arguments:
            field:
                The foreign key field to get or create.
            parameters:
                The construction / query arguments. These parameters are shared among
                all constructions.
            tree:
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes
            dry_run:
                Do not insert in database.
            _recursion_level:
                This key is used internaly to track number of recursions.

        Example:

            .. code::

                class B(Base):
                    key2 = IntegerField() # or ForeignKey(C)

                class A(Base):
                    key1 = ForeignKey(B)

                tree={"key1": "B"}
                # or if B also depends on Foreign Keys
                tree={"key1": "B", "key1.key2": "C"}
                ```
        """
        tree = tree or {}

        sub_class_name = tree.get(field.name, None)
        if sub_class_name is not None:
            sub_tree = cls.get_sub_info(field.name, tree)

            # get general parameters
            sub_pars = {
                key: val for key, val in parameters.items() if len(key.split(".")) == 1
            }
            # now update keys with more specialized keys
            sub_pars.update(cls.get_sub_info(field.name, parameters))

            instance, created = field.related_model.get_or_create_from_parameters(
                sub_pars,
                tree=sub_tree,
                dry_run=dry_run,
                _class_name=sub_class_name,
                _recursion_level=_recursion_level,
            )

        else:
            instance, created = None, False
            if not field.null:
                raise KeyError(
                    "Tree for parsing classes did not contain"
                    f" value for non-null foreign key {field.name}"
                )

        return instance, created

    @classmethod
    @transaction.atomic
    def get_or_create_from_parameters(  # pylint: disable=C0202, R0913, R0914, R0912
        calling_cls,
        parameters: Dict[str, Any],
        tree: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        _class_name: Optional[str] = None,
        _recursion_level: int = 0,
    ) -> Tuple["Base", bool]:
        """Creates class and dependencies through top down approach from parameters.

        Arguments:
            calling_cls:
                The top class which starts the get or create chain.

            parameters:
                The construction / query arguments.
                These parameters are shared among all constructions.

            tree:
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes

            dry_run:
                Do not insert in database.

            _class_name:
                This key is used internaly to identified the specialization
                of the base object.

            _recursion_level:
                This key is used internaly to track number of recursions.

        Populates columns from parameters and recursevily creates foreign keys need for
        construction.
        Foreign keys must be specified by the tree in order to instanciate the right
        tables.
        In case some tables have shared column names but want to use differnt values,
        use the `specialized_parameters` argument.
        This routine does not populate many to many keys.

        Example:

            Below you can find an example how this method works.

            .. code-block:: python

                class BA(BaseB):
                    b1 = IntegerField()
                    b2 = IntegerField()

                class BB(BaseB):
                    b1 = IntegerField()
                    b2 = IntegerField()
                    b3 = IntegerField()

                class C(BaseC):
                    c1 = IntegerField()
                    c2 = ForeignKey(BaseB)

                class A(BaseA):
                    a = IntegerField()
                    b1 = ForeignKey(BaseB)
                    b2 = ForeignKey(BaseB)
                    c = ForeignKey(BaseC)

                instance, created = A.get_or_create_from_parameters(
                    parameters={"a": 1, "b1": 2, "b2": 3, "b3": 4, "c1": 5, "b2.b2": 10},
                    tree={
                        "b1": "BA",
                        "b2": "BB",
                        "c": "C",
                        "c.c2": "BA"
                    }
                )


            will get or create the instances

            .. code-block:: python

                a0 = A.objects.all()[-1]
                a0 == instance

                a0.a == 1        # key of A from pars
                a0.b1.b1 == 2    # a.b1 is BA through tree and a.b1.b1 is two from pars
                a0.b1.b2 == 3
                a0.b2.b1 == 2    # a.b2 is BB through tree and a.b1.b1 is two from pars
                a0.b2.b2 == 10   # a.b2.b2 is overwriten by specialized parameters
                a0.b2.b3 == 4
                a0.c.c1 == 5     # a.c is C through tree
                a0.c.c2.b1 == 2  # a.c.c2 is BA through tree
                a0.c.c2.b2 == 3
        """
        # parse full dependency and warn if duplicate columns
        indent = "|" if _recursion_level else ""
        indent += "-" * _recursion_level * 2

        cls = (
            calling_cls._get_child_by_name(_class_name) if _class_name else calling_cls
        )

        if _recursion_level == 0:
            for key, tables in cls.get_recursive_columns(tree).items():
                if len(tables) > 1:
                    LOGGER.debug(
                        "Column %s is used by the following tables %s", key, tables
                    )

        LOGGER.debug("%sPreparing creation of %s", indent, cls)

        kwargs = {}
        for field in cls.get_open_fields():

            if isinstance(field, models.ForeignKey):
                instance, created = cls._get_or_create_fk(  # pylint: disable=W0212
                    field,
                    parameters,
                    tree=tree,
                    dry_run=dry_run,
                    _recursion_level=_recursion_level + 1,
                )
                kwargs[field.name] = instance

            else:
                value = parameters.get(field.name, None)
                if value is None and not (
                    field.null or isinstance(field, models.ManyToManyField)
                ):
                    raise KeyError(
                        f"Missing value for constructing {cls}."
                        f" Parameter dictionary has no value for {field.name}."
                        f" Here are the keys {parameters.keys()}."
                    )
                elif value is not None:
                    kwargs[field.name] = field.get_db_prep_value(value, connection)

        try:
            instance, created = cls.objects.get_or_create(**kwargs)
        except Exception as e:
            LOGGER.error(
                "Get or create call for %s failed with kwargs\n%s", cls, kwargs
            )
            raise e

        LOGGER.debug(
            "%sCreated %s" if created else "%sFetched %s from db", indent, instance
        )

        return instance, created
