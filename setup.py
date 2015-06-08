#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = '0.1.0'

install_requires = [
    'djangorestframework>=2.3.14',
]


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
)
