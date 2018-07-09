#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = '1.2.0'

install_requires = [
    'djangorestframework>=3.0.0,<4',
]


# note: These are all byte-strings on python 2, and unicode on python 3.
# ... and that's how setuptools likes it. https://bugs.python.org/setuptools/issue152
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
    install_requires=install_requires,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
