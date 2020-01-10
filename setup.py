#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = '2.0.0'


setup(
    name='rest-framework-generic-relations',
    version=version,
    url='https://github.com/Ian-Foote/rest-framework-generic-relations',
    license='BSD',
    description='Generic Relations for Django Rest Framework',
    author='Ian Foote',
    author_email='python@ian.feete.org',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['djangorestframework>=3.8.0'],
    python_requires='>=3.4',
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
