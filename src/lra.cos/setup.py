# -*- coding: utf-8 -*-
"""Installer for the ade25.base package."""

from setuptools import find_packages
from setuptools import setup

import os


version = '1.0.0.dev0'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = \
    read('README.rst') + '\n\n' + \
    read('CHANGES.rst')

setup(
    name='lra.cos',
    version='1.0.0',
    description="LRA: Consulting on Schedule",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone, Python, Utilities',
    author='Christoph Boehner-Figas',
    author_email='cb@ade25.de',
    url='https://github.com/a25kk/lra.git',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['lra'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'babel',
        'setuptools',
        'plone.app.dexterity [relations]',
        'plone.app.relationfield',
        'plone.namedfile [blobs]',
        'pytz',
        'mysqlclient',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'coverage',
            'flake8',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.PDBDebugMode',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
