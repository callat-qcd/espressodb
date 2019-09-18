"""Script to completely whipe migrations.
"""
from django.core.management.base import BaseCommand
from espressodb.base.utilities.version import get_db_info, get_repo_version


class Command(BaseCommand):

    helps = "Returns espressodb version infos and db access"

    def handle(self, *args, **options):
        name, user = get_db_info()
        branch, version = get_repo_version()
        print(f"espressodb version: {version} ({branch})\nDB access: {user}@{name}")
