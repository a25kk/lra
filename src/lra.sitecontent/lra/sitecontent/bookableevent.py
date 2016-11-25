# -*- coding: utf-8 -*-
"""Module providing bookable event content type"""

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer


class IBookableEvent(model.Schema, IImageScaleTraversable):
    """
        A event content type that offers bookings via web form
    """


@implementer(IBookableEvent)
class BookableEvent(Container):
    pass
