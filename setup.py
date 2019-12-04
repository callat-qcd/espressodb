# -*- coding: utf-8 -*-
"""Setup file for EspressoDB
"""
from espressodb import __version__

__author__ = "@cchang5, @ckoerber"


from os import path

from setuptools import setup, find_packages

CWD = path.abspath(path.dirname(__file__))

with open(path.join(CWD, "README.md"), encoding="utf-8") as inp:
    LONG_DESCRIPTION = inp.read()

with open(path.join(CWD, "requirements.txt"), encoding="utf-8") as inp:
    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]

with open(path.join(CWD, "requirements-dev.txt"), encoding="utf-8") as inp:
    REQUIREMENTS_DEV = [el.strip() for el in inp.read().split(",")]


setup(
    name="espressodb",
    python_requires=">=3.6",
    version=__version__,
    description=None,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/callat-qcd/espressodb",
    project_urls={
        "Bug Reports": "https://github.com/callat-qcd/espressodb/issues",
        "Source": "https://github.com/callat-qcd/espressodb",
        "Documentation": "https://espressodb.readthedocs.io",
    },
    author=__author__,
    author_email="ckoerber@berkeley.edu",
    keywords=["Database", "Workflow", "Django"],
    packages=find_packages(exclude=["docs", "tests", "example"]),
    install_requires=REQUIREMENTS,
    entry_points={"console_scripts": ["espressodb=espressodb.manage:main"]},
    extras_require={"dev": REQUIREMENTS_DEV},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
    ],
    include_package_data=True,
)
