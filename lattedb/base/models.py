# pylint: disable=C0111, R0903, E1101
"""Lattice structure tables
"""
from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional
from typing import Any

import logging

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django_pandas.managers import DataFrameManager
from django.db import connection

from django.db.utils import IntegrityError

LOGGER = logging.getLogger("base")


class Base(models.Model):
    """ Mother of all tables
    """

    id = models.AutoField(primary_key=True)
    type = models.TextField(editable=False)  # autofield by inheritance
    last_modified = models.DateTimeField(auto_now=True)  # also update
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    tag = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

    objects = DataFrameManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Default init but adds specialization attribute
        """
        super().__init__(*args, **kwargs)
        self._specialization = None

    @classmethod
    def get_open_fields(cls) -> List["Field"]:
        """Returns keys which are editable and non ForeignKeys
        """
        fields = []
        for field in cls._meta.get_fields():  # pylint: disable=W0212
            if not (
                field.name in ["id", "type", "user"]
                or not field.editable
                or field.name.endswith("_ptr")
            ):
                fields.append(field)
        return fields

    def __str__(self) -> str:
        """Verbose description of instance name, parent and column values.
        """
        kwargs = {
            field.name: getattr(self, field.name)
            for field in self.get_open_fields()
            if getattr(self, field.name) is not None
            and not isinstance(field, models.ForeignKey)
        }
        base = (
            f"[{self.__class__.mro()[1].__name__}]"
            if type(self) != Base  # pylint: disable=C0123
            else ""
        )
        info = ", ".join([f"{key}={val}" for key, val in kwargs.items()])
        return f"{self.__class__.__name__}{base}({info})"

    def clean(self):
        """Sets the type name to the class instance name
        """
        self.type = self.__class__.__name__

    @property
    def specialization(self):
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
        """Compares name of cls and all subclasses to `class_name` and returns match

        **Arguments**
            class_name=str
                The name to match

        **Raises**
            KeyError:
                In case no or more then one class matches the name.
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
        cls, key: str, tree: Dict[str, Any]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Extracts the class name and sub tree for a given tree and key

        **Arguments**
            key: str
                The key to look up in the dictionary

            tree: Dict[str, Any]
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes

        **Raises**
            TypeError:
                If the values of the dictionary are not of type string or Tuple

            KeyError:
                If the key was not found in the dictionary
        """
        sub_tree_info = tree.get(key, None)
        if sub_tree_info is not None:
            if isinstance(sub_tree_info, tuple) and len(sub_tree_info) == 2:
                sub_class_name, sub_tree = sub_tree_info
            elif isinstance(sub_tree_info, str):
                sub_class_name, sub_tree = sub_tree_info, None
            else:
                raise TypeError(
                    "Error in parsing dependency tree."
                    " Sub class info must be either a tuple of type str"
                    " and dictionary or a string."
                    f" received {type(sub_tree_info)}"
                )
        else:
            raise KeyError(
                "Key '%s' was not specified in tree but needed for instantiating %s"
                % (key, cls)
            )

        return sub_class_name, sub_tree

    @classmethod
    def get_recursive_columns(
        cls, tree: Optional[Dict[str, Any]] = None, _class_name: Optional[str] = None
    ) -> Tuple[Dict[str, List[str]]]:
        """Recursively parses table including foreign keys to extract all column names.

        **Arguments**
            tree: Optional[Dict[str, Any]] = None
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes

            _class_name: Optional[str] = None
                This key is used internaly to identified the specialization of the base
                object.
        """
        tree = tree or {}

        specialization = cls._get_child_by_name(_class_name) if _class_name else cls

        columns = {}
        for field in specialization.get_open_fields():
            if isinstance(field, models.ForeignKey):

                sub_class_name, sub_tree = specialization.get_sub_info(field.name, tree)
                if sub_class_name is not None:
                    for key, val in field.related_model.get_recursive_columns(
                        tree=sub_tree, _class_name=sub_class_name
                    ).items():
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
        specialized_parameters: Dict[str, Any] = None,
        dry_run: bool = False,
        _recursion_level: int = 0,
    ):
        """Recursively iterates ForeignKey field and tries to construc the foreign keys
        from parameters and parse tree using `get_or_create_from_parameters`.

        **Arguments**
            field: models.ForeignKey
                The foreign key field to get or create.

            parameters: Dict[str, Any]
                The construction / query arguments. These parameters are shared among
                all constructions.

            tree: Optional[Dict[str, Any]] = None
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes

                Example:
                ```
                class B(Base):
                    key2 = IntegerField() # or ForeignKey(C)

                class A(Base):
                    key1 = ForeignKey(B)

                tree={"key1": "B"}
                # or if B also depends on Foreign Keys
                tree={"key1": ("B", {"key2": "C"})}
                ```

            specialized_parameters: Dict[str, Any] = None
                The construction / query arguments for special foreign keys (in case
                there is overlap). Follows a similar syntax as the tree.

                Example:
                ```
                class B(Base):
                    key2 = IntegerField()

                class A(Base):
                    key1 = ForeignKey(B)

                specialized_parameters={"key1": {"key2": 2}}
                ```

            dry_run: bool = False
                Do not insert in database.

            _recursion_level: int = 0
                This key is used internaly to track number of recursions.
        """
        tree = tree or {}

        for key, tables in cls.get_recursive_columns(tree).items():
            if len(tables) > 1:
                LOGGER.info("Column %s is used by the following tables %s", key, tables)

        if specialized_parameters is not None:
            raise NotImplementedError(
                "Overwriting of default kwargs not yet implmented."
            )

        sub_class_name, sub_tree = cls.get_sub_info(field.name, tree)
        if sub_class_name is not None:
            instance, all_instances = field.related_model.get_or_create_from_parameters(
                parameters,
                tree=sub_tree,
                specialized_parameters=specialized_parameters,
                dry_run=dry_run,
                _class_name=sub_class_name,
                _recursion_level=_recursion_level,
            )

        else:
            instance, all_instances = None, []
            if not field.null:
                raise KeyError(
                    "Tree for parsing classes did not contain"
                    f" value for non-null foreign key {field.name}"
                )

        return instance, all_instances

    @classmethod
    def get_or_create_from_parameters(  # pylint: disable=C0202, R0913, R0914
        calling_cls,
        parameters: Dict[str, Any],
        tree: Optional[Dict[str, Any]] = None,
        specialized_parameters: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        _class_name: Optional[str] = None,
        _recursion_level: int = 0,
    ) -> Tuple["Base", List[Tuple["Base", bool]]]:
        """Creates class and dependencies through top down approach from parameters.

        Populates columns from parameters and recursevily creates foreign keys need for
        construction.
        Foreign keys must be specified by the tree in order to instanciate the right
        tables.
        In case some tables have shared column names but want to use differnt values,
        use the `specialized_parameters` argument.

        **Example**
            ```
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

            instance, instances = A.get_or_create_from_parameters(
                parameters={"a": 1, "b1": 2, "b2": 3, "b3": 4, "c1": 5},
                tree={"b1": "BA", "b2": "BB", "c": ("C", {"c2": "BA"})}
                specialized_parameters={"b2": {"b2": 10}}
            )
            ```
            will get or create the instances
            ```
            a = A.objects.all()[-1]
            a == instance
            a == instances[-1]

            a.a == 1        # key of A from pars
            a.b1.b1 == 2    # a.b1 is BA through tree and a.b1.b1 is two from pars
            a.b1.b2 == 3
            a.b2.b1 == 2    # a.b2 is BB through tree and a.b1.b1 is two from pars
            a.b2.b2 == 10   # a.b2.b2 is overwriten by specialized_parameters
            a.b2.b3 == 4
            a.c.c1 == 5     # a.c is C through tree
            a.c.c2.b1 == 2  # a.c.c2 is BA through tree
            a.c.c2.b2 == 3
            ```

        **Arguments**
            calling_cls: Base
                The top class which starts the get or create chain.

            parameters: Dict[str, Any]
                The construction / query arguments. These parameters are shared among
                all constructions.

            tree: Optional[Dict[str, Any]] = None
                The tree of ForeignKey dependencies. This specify which class the
                ForeignKey will take since only the base class is linked against.
                Keys are strings corresponding to model fields, values are either
                strings corresponding to classes

            specialized_parameters: Dict[str, Any] = None
                The construction / query arguments for special foreign keys (in case
                there is overlap). Follows a similar syntax as the tree.

            dry_run: bool = False
                Do not insert in database.

            _class_name: Optional[str] = None
                This key is used internaly to identified the specialization of the base
                object.

            _recursion_level: int = 0
                This key is used internaly to track number of recursions.
        """
        # parse full dependency and warn if duplicate columns
        indent = "|" if _recursion_level else ""
        indent += "-" * _recursion_level * 2

        if specialized_parameters is not None:
            raise NotImplementedError(
                "Overwriting of default kwargs not yet implmented."
            )

        cls = calling_cls._get_child_by_name(_class_name) if _class_name else calling_cls

        LOGGER.debug("%sPreparing creation of %s", indent, cls)

        kwargs = {}
        all_instances = []
        for field in cls.get_open_fields():
            if isinstance(field, models.ForeignKey):

                instance, instances = cls._get_or_create_fk(  # pylint: disable=W0212
                    field,
                    parameters,
                    tree=tree,
                    specialized_parameters=specialized_parameters,
                    dry_run=dry_run,
                    _recursion_level=_recursion_level + 1,
                )
                all_instances += instances
                kwargs[field.name] = instance

            else:
                value = parameters.get(field.name, None)
                if value is None and not field.null:
                    raise KeyError(
                        f"Missing value for constructing {cls}."
                        f" Parameter dictionary has no value for {field.name}"
                    )
                elif value is not None:
                    kwargs[field.name] = field.get_db_prep_value(value, connection)

        try:
            instance, not_exist = cls.objects.get_or_create(**kwargs)
        except IntegrityError as e:
            LOGGER.debug("Get or create call for %s failed with kwargs\n%s", cls, kwargs)
            raise e

        if not_exist:
            LOGGER.debug("%sCreated %s", indent, instance)
        else:
            LOGGER.debug("%sFetched %s from db", indent, instance)

        if not dry_run and not_exist:
            instance.save()
        all_instances.append((instance, not_exist))

        return instance, all_instances
