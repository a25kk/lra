# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from z3c.relationfield import RelationChoice
from zope import schema
from zope.interface import Interface, provider

from lra.cos import _


@provider(IFormFieldProvider)
class ILRAWidgetConsultationSchedule(Interface):
    """ Content Widget Consultation appointments schedule """
    pass
