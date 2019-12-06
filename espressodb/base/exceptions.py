"""Custom exceptions used in EspressoDB
"""
from typing import Optional, Dict, Any

from django.db.models import Model


class ConsistencyError(Exception):
    """Error which is raised during consistency checks.

    The consistency checks are called when a model is saved or created with the `safe`
    option.
    This Error wraps individual exceptions to provide more verbose information.
    """

    def __init__(
        self, error: Exception, instance: Model, data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize consistency error and prepares custom error method.

        Arguments:
            error: The original Exception which was raised by the check
            model: The model which raises the check
            data: The data the model was checked with.
        """
        ddata = {
            field.name: getattr(instance, field.name)
            for field in instance.get_open_fields()
        }
        if data is not None:
            ddata.update(data)

        message = f"Consistency error when checking {instance.__class__}.\n"
        message += f"{type(error).__name__}"
        message += f":\n\t{error}\n" if str(error) else "\n"
        if ddata:
            message += "Data used for check:\n\t* "
            message += "\n\t* ".join([f"{key}: {val}" for key, val in ddata.items()])

        super().__init__(message)

        self.data = ddata
        self.instance = instance
        self.error = error
