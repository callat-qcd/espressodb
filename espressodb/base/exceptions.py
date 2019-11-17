"""Custom exceptions used in EspressoDB
"""
from typing import Optional, Dict, Any

from espressodb.base.models import Base


class ConsistencyError(Exception):
    """Error which is raised during consistency checks.

    The consistency checks are called when a model is saved or created with the `safe`
    option.
    This Error wraps individual exceptions to provide more verbose information.
    """

    def __init__(
        self, error: Exception, model: Base, data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize consistency error and prepares custom error method.

        Arguments:
            error: The original Exception which was raised by the check
            model: The model which raises the check
            data: The data the model was checked with.
        """
        data = data or {}
        message = f"Consistency error when checking {model}.\n"
        message += f"{type(error).__name__}"
        message += f":\n\t{error}\n" if str(error) else "\n"
        if data:
            message += "Data used for check:\n\t* "
            message += "\n\t* ".join([f"{key}: {val}" for key, val in data.items()])

        super().__init__(message)

        self.data = data
        self.model = model
        self.error = error
