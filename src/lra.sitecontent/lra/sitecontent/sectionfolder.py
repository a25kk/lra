# -*- coding: utf-8 -*-
"""Module providing section folder content type"""

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer

from lra.sitecontent import MessageFactory as _


class ISectionFolder(form.Schema, IImageScaleTraversable):
    """
    A folder acting as dedicated site section
    """


@implementer(ISectionFolder)
class SectionFolder(Container):
    pass
