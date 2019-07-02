"""Command to build the docs.
"""

import os
import logging

from bs4 import BeautifulSoup
from sphinx.application import Sphinx

from django.core.management.base import BaseCommand

from lattedb.config.settings import BASE_DIR, PROJECT_APPS


LOGGER = logging.getLogger("main.commands")

RST_TEMPLATE = r"""####################
{app_name}
####################

.. toctree::
   :maxdepth: 4
   :glob:

.. automodule:: lattedb.{app_name}.models
   :members:
   :show-inheritance:
"""


class Command(BaseCommand):
    """Start a new application in the project base dir
    """

    help = "Creates doc pages for all installed models"
    sourcedir = os.path.join(BASE_DIR, "documentation", "source")
    confdir = os.path.join(BASE_DIR, "documentation", "source")
    outputdir = os.path.join(BASE_DIR, "documentation", "source", "_build")
    doctreedir = os.path.join(BASE_DIR, "documentation", "source", "_build")
    builder = "html"

    doc_dir = os.path.join(BASE_DIR, "documentation", "templates", "apps")
    exclude = ("base", "admin", "documentation")

    def handle(self, *args, **options):
        """Installs app in `lattedb`
        """
        for app in PROJECT_APPS:
            app_name = app.split(".")[-1]
            if not app_name in self.exclude:
                rst_address = os.path.join(self.sourcedir, "apps", app_name + ".rst")
                with open(rst_address, "w") as fout:
                    fout.write(RST_TEMPLATE.format(app_name=app_name))

        Sphinx(
            self.sourcedir, self.confdir, self.outputdir, self.doctreedir, self.builder
        ).build()

        app_doc_dir = os.path.join(self.outputdir, "apps")
        for doc_file in os.listdir(app_doc_dir):

            if not doc_file.endswith(".html") or "index" in doc_file:
                continue

            with open(os.path.join(app_doc_dir, doc_file), "r") as fin:
                soup = BeautifulSoup(fin.read(), "lxml")

            html = soup.find("div", attrs={"role": "main"})

            with open(os.path.join(self.doc_dir, doc_file), "w") as fout:
                fout.write(html.prettify())
