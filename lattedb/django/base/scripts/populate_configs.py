# pylint: disable=E1101
"""Example script on how to populate configs.
"""
import logging

import django


LOGGER = logging.getLogger(__name__)


def main():
    """Populates the databaes with example inputs

    This is currently quite boring since most of the tables do not have actual elements.
    """
    django.setup()


if __name__ == "__main__":
    main()
