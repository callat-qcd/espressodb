"""Script to return version info.
"""
from django.core.management.base import BaseCommand

from espressodb.management.utilities.version import get_db_info, get_repo_version


class Command(BaseCommand):

    helps = "Returns espressodb version infos and db access"

    def handle(self, *args, **options):

        branch, version = get_repo_version()
        info = f"espressodb version: {version} ({branch})"

        name, user = get_db_info()
        if name:
            info += "\nDB access:"
            info += f"{user}@" if user else " "
            info += f"{name}"

        print(info)
