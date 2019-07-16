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

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    class Meta:
        abstract = True

    def clean(self):
        """Sets the type name to the class instance name
        """
        self.type = self.__class__.__name__

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
    def _get_or_creage_fk(  # pylint: disable=R0913
        cls,
        field: models.ForeignKey,
        parameters: Dict[str, Any],
        tree: Optional[Dict[str, Any]] = None,
        overwrite: Dict[str, Any] = None,
        dry_run: bool = False,
    ):
        """
        """
        tree = tree or {}

        LOGGER.debug("Parsing FK field %s", field.name)

        sub_class_info = tree.get(field.name, None)
        if sub_class_info is not None:
            if isinstance(sub_class_info, tuple) and len(sub_class_info) == 2:
                sub_class_name, sub_tree = sub_class_info
            elif isinstance(sub_class_info, str):
                sub_class_name, sub_tree = sub_class_info, None
            else:
                raise ValueError(
                    "Error in parsing dependency tree."
                    " Sub class info must be either a tuple of type str"
                    " and dictionary or a string."
                    f" received {type(sub_class_info)}"
                )

            instance, all_instances = field.related_model.get_or_create_from_parameters(
                parameters,
                tree=sub_tree,
                class_name=sub_class_name,
                overwrite=overwrite,
                dry_run=dry_run,
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
    def get_or_create_from_parameters(  # pylint: disable=C0202, R0913
        calling_cls,
        parameters: Dict[str, Any],
        tree: Optional[Dict[str, Any]] = None,
        class_name: Optional[str] = None,
        overwrite: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
    ) -> List[Tuple[models.Model, bool]]:
        """
        """
        # parse full dependency and warn if duplicate columns

        LOGGER.debug(
            "Receiving `get_or_create_from_parameters` from %s for %s",
            calling_cls,
            class_name,
        )

        cls = calling_cls._get_child_by_name(class_name) if class_name else calling_cls

        kwargs = {}
        all_instances = []
        for field in cls._meta.get_fields():  # pylint: disable=W0212
            if (
                field.name in ["id", "type", "user"]
                or not field.editable
                or field.name.endswith("_ptr")
            ):
                continue

            if isinstance(field, models.ForeignKey):

                instance, instances = cls._get_or_creage_fk(  # pylint: disable=W0212
                    field, parameters, tree=tree, overwrite=overwrite, dry_run=dry_run
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
                    kwargs[field.name] = value

        if overwrite is not None:
            raise NotImplementedError(
                "Overwriting of default kwargs not yet implmented."
            )

        LOGGER.debug("Trying get or create for %s with kwargs %s", cls, kwargs)
        instance, not_exist = cls.objects.get_or_create(**kwargs)
        if not_exist:
            LOGGER.debug("Created %s", instance)
        else:
            LOGGER.debug("Fetched %s from db", instance)

        if not dry_run and not_exist:
            LOGGER.debug("Trying to save %s", instance)
            instance.save()
        all_instances.append((instance, not_exist))

        return instance, all_instances
