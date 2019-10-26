"""Tools to keep track of the current repository version and database.
"""
from typing import Tuple
from typing import Optional

import subprocess
import os

from django.conf import settings

DATABASES = getattr(settings, "DATABASES", {})

_FILE_PATH = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(
    os.path.join(_FILE_PATH, os.pardir, os.pardir, os.pardir, ".git")
)


def get_repo_version() -> Tuple[Optional[str], Optional[str]]:
    """Finds information about the EspressoDB repository if possible.

    Only works if EspressoDB is installed from the github repository.

    Returns:
        The branch and the git tag-commit version as strings if found.
        If not installed (and symlinked from the repo), returns the PyPi version.
    """

    tag_commit_cmd = ["git", f"--git-dir={BASE_DIR}", "describe", "--always", "--long"]
    branch_cmd = ["git", f"--git-dir={BASE_DIR}", "rev-parse", "--abbrev-ref", "HEAD"]

    try:
        tag_commit = (
            subprocess.check_output(tag_commit_cmd, stderr=subprocess.DEVNULL)
            .decode("utf-8")
            .strip()
        )
        branch = (
            subprocess.check_output(branch_cmd, stderr=subprocess.DEVNULL)
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        from espressodb import __version__

        tag_commit = __version__
        branch = None

    return branch, tag_commit


def get_db_info() -> Tuple[Optional[str], Optional[str]]:
    """Extract database informations from the settings.

    Returns:
        The name of the db and the name of the db user if found.

    Note:
        ``.sqlite`` databases do not specify a user.
    """
    db = DATABASES.get("default", {})
    name, user = db.get("NAME"), db.get("USER")
    if name is not None and os.sep in name:
        name = name.split(os.sep)[-1]
    return name, user
