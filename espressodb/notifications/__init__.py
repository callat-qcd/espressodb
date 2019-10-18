"""The notification module provides a Python logging.Logger like class which stores and
reads information to the database.

Example:
    The notfier works just like a Logger, e.g.,

    .. code-block::

        notifier = get_notifier()
        notifier.info("Hello world!", title="Test the notifier")

    See also the :class:`espressodb.notifications.models.Notifier` class for more
    information.
"""
from typing import Optional
from typing import List

# needed for type annotation
import espressodb


def get_notifier(
    tag: Optional[str] = None,
    groups: Optional[List[str]] = None,
    fail_if_not_exists: bool = True,
) -> "espressodb.notifications.models.Notifier":
    """Get a notifier instance.

    Arguments:
        tag:
            The tag of the notification. Used for fast searches.
        groups:
            The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
        fail_if_not_exists:
            If the user specifies group names which are not found,
            the default behavior is that storing of notfications will fail
            (e.g., raising KeyErrors).
            If this is set to False, the code progress but logs Notifications to other
            groups.

    Returns:
        A notifier instance
    """
    from espressodb.notifications.models import Notifier

    return Notifier(tag=tag, groups=groups, fail_if_not_exists=fail_if_not_exists)
