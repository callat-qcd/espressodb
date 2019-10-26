"""Script to return EspressoDB and database version info.
"""
from django.core.management.base import BaseCommand

from espressodb.management.utilities.version import get_db_info, get_repo_version


class Command(BaseCommand):
    """Prints espressodb version and db access infos

    Uses :meth:`espressodb.management.utilities.version.get_repo_version`
    and :meth:`espressodb.management.utilities.version.get_db_info`.
    """

    helps = "Prints espressodb version and db access infos"

    def handle(self, *args, **options):
        branch, version = get_repo_version()
        info = f"espressodb version: {version}" + (f" ({branch})" if branch else "")

        name, user = get_db_info()
        if name:
            info += "\nDB access:"
            info += f"{user}@" if user else " "
            info += f"{name}"

        print(info)
