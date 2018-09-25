# -*- coding: utf-8 -*-
"""Module providing bookable event content type"""

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer
from zope import schema

from lra.sitecontent import _


class IBookableEvent(model.Schema, IImageScaleTraversable):
    """
        A event content type that offers bookings via web form
    """
    contact_email = schema.TextLine(
        title=_(u"Recipient E-Mail"),
        required=True
    )
    additional_label = schema.TextLine(
        title=_(u"Additional Field Label"),
        description=_(u"Override default filed label for text field."),
        required=False
    )
    additional_description = schema.TextLine(
        title=_(u"Additional Field Description (optional)"),
        description=_(u"Add optional help text on required data."),
        required=False
    )

    privacy_note = schema.Text(
        title=_(u"Custom Privacy and Data Protection Note"),
        description=_(u"Add optional help text to outline context specific "
                      u"regulations concerning the site's privacy and "
                      u"data protection policies."),
        required=False
    )


@implementer(IBookableEvent)
class BookableEvent(Container):
    pass
