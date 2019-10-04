"""Fast access to Notifier
"""
from typing import Optional
from typing import List


def get_notifier(
    tag: Optional[str] = None,
    groups: Optional[List[str]] = None,
    fail_if_not_exists: bool = True,
):
    """returns the Notifier class

    :param tag: The tag of the notification. Used for fast searches.
    :param groups: The user groups which are allowed to view this notfication.
        No groups means not logged in users are able to view the notfication.
    :param fail_if_not_exists: If the user specifies group names which are not found,
        the default behavior is that storing of notfications will fail
        (e.g., raising KeyErrors).
        If this is set to False, the code progress but logs Notifications to other
        groups.
    """
    from espressodb.notifications.models import Notifier

    return Notifier(tag=tag, groups=groups, fail_if_not_exists=fail_if_not_exists)
