#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import abspath, dirname, join


def read_relative_file(filename):
    """
    Returns contents of the given file, whose path is supposed relative
    to this module.
    """
    with open(join(dirname(abspath(__file__)), filename), "r") as f:
        return f.read()


setup(
    name="rest-framework-generic-relations",
    version="2.0.0",
    url="https://github.com/Ian-Foote/rest-framework-generic-relations",
    license="BSD",
    description="Generic Relations for Django Rest Framework",
    long_description=read_relative_file("README.md"),
    long_description_content_type="text/markdown",
    author="Ian Foote",
    author_email="python@ian.feete.org",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["djangorestframework>=3.11.0"],
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
