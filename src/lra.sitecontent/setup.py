# -*- coding: utf-8 -*-
"""Installer for the lra.sitecontent package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read('README.rst')

setup(
    name='lra.sitecontent',
    version='1.0.0',
    description="Sitecontent package containing folderish content pages",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone Dexterity',
    author='Christoph Boehner',
    author_email='cb@vorwaerts-werbung.de',
    url='http://pypi.python.org/pypi/lra.sitecontent',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['lra'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.api',
        'plone.app.dexterity [relations]',
        'plone.app.relationfield',
        'plone.namedfile [blobs]',
        'plone.formwidget.contenttree',
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
            'jarn.mkrelease',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'Sphinx',
            'zest.releaser',
            'zptlint',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
