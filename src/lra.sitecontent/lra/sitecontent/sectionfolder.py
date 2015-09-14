# -*- coding: utf-8 -*-
"""Module providing section folder content type"""

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer


class ISectionFolder(model.Schema, IImageScaleTraversable):
    """
    A folder acting as dedicated site section
    """


@implementer(ISectionFolder)
class SectionFolder(Container):
    pass
