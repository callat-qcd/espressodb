"""Tools to keep track of the current repository version
"""
from typing import Tuple

import subprocess
import os

try:
    from django.conf.settings import DATABASES
except ImportError:
    DATABASES = {}

_FILE_PATH = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(
    os.path.join(_FILE_PATH, os.pardir, os.pardir, os.pardir, ".git")
)


def get_repo_version() -> Tuple[str, str]:
    """Returns the branch and the git tag-commit version of the repository if still
    linked.
    """

    tag_commit_cmd = ["git", f"--git-dir={BASE_DIR}", "describe", "--always", "--long"]
    branch_cmd = ["git", f"--git-dir={BASE_DIR}", "rev-parse", "--abbrev-ref", "HEAD"]

    try:
        tag_commit = subprocess.check_output(tag_commit_cmd).decode("utf-8").strip()
        branch = subprocess.check_output(branch_cmd).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        tag_commit = branch = None

    return branch, tag_commit


def get_db_info() -> Tuple[str, str]:
    """Returns the name of the DB and the user
    """
    db = DATABASES.get("default", {})
    return db.get("NAME"), db.get("USER")