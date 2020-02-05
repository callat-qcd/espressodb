"""Signal processing functions for the base class

Includes checks to run on save.
"""
from django.db.models import Model
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver

from espressodb.base.models import Base
from espressodb.base.exceptions import ConsistencyError


@receiver(pre_save)
def base_save_handler(sender: Base, **kwargs):
    """Runs pre save logic of Base class

    This calls the ``.pre_save()`` and  ``.check_consistency()`` method of the instance.
    """
    if not issubclass(sender, Base):
        return

    instance = kwargs.get("instance")
    if instance is None:
        return

    if instance.run_pre_save:
        instance.pre_save()

    if instance.run_checks:
        try:
            instance.check_consistency()
        except Exception as error:
            raise ConsistencyError(error, instance)


@receiver(m2m_changed)
def base_m2m_add_handler(sender: Model, **kwargs):
    """Runs many to many pre add logic of Base class

    This calls the check_m2m_consistency method of the class containing the m2m column.

    Note:
        For revese adding elements, the pk_set is sorted.
    """
    if kwargs.get("action") != "pre_add":
        return

    model = kwargs.get("model")
    instance = kwargs.get("instance")
    reverse = kwargs.get("reverse")
    pk_set = kwargs.get("pk_set")

    if model is None or instance is None or reverse is None or pk_set is None:
        return

    # Identify the class which implments the m2m
    m2m_cls = model if reverse else instance.__class__

    if not issubclass(m2m_cls, Base):
        return

    if not m2m_cls.run_checks:
        return

    # Identify the name of the m2m attr within this class
    through_table = sender._meta.db_table  # pylint: disable=W0212
    column = None
    for field in m2m_cls.get_open_fields():
        if field.many_to_many and field.m2m_db_table() == through_table:
            column = field.name
            break

    if reverse:
        # a1.check_m2m_consistency((b,))
        # a2.check_m2m_consistency((b,))
        instances_to_add = instance.__class__.objects.filter(pk=instance.pk)
        for pk in sorted(pk_set):
            instance = m2m_cls.objects.get(pk=pk)
            try:
                instance.check_m2m_consistency(instances_to_add, column=column)
            except Exception as error:
                raise ConsistencyError(
                    error,
                    instance,
                    data={"instances_to_add": instances_to_add, "column": column},
                )

    else:
        # b.check_m2m_consistency((a1, a2, ...))
        instances_to_add = model.objects.filter(pk__in=pk_set)
        try:
            instance.check_m2m_consistency(instances_to_add, column=column)
        except Exception as error:
            raise ConsistencyError(
                error,
                instance,
                data={"instances_to_add": instances_to_add, "column": column},
            )
