#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


def get_version():
    with open("getmymsg/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="getmymsg_client",
    version=get_version(),
    description="Cliente de práctica 3 de curso de Sistemas Distribuidos.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Pedro Faria",
    author_email="pjfaria.17@est.ucab.edu.ve or pjfariakiddo@gmail.com",
    license="GPLv3",
    url="https://github.com/SatoshiKiddo/getmymsg_client",
    python_requires='>=2.7',
    packages=find_packages(),
    install_requires=[
        "PyYAML>=5.3.1",
    ],
    entry_points={
        "console_scripts": [
            "getmymsg-client = getmymsg:main",
        ]
    },
)

