# -*- coding: utf-8 -*-
"""Module providing bookable event content type"""
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer
from zope import schema

from lra.cos import _


class IConsultingSchedule(model.Schema, IImageScaleTraversable):
    """
        A event content type that offers bookings via web form
    """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    description = schema.Text(
        title=_(u"Description"),
        description=_(u"Short and highlighted teaser message"),
        required=False,
    )
    fieldset(
        'details',
        label=_(u"Details"),
        fields=['text', ]
    )
    text = RichText(
        title=_(u"Extended information"),
        required=False,
    )

    fieldset(
        'media',
        label=_(u"Media"),
        fields=['image', 'image_caption']
    )

    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload preview image that can be used in search "
                      u"results and listings."),
        required=False
    )

    image_caption = schema.TextLine(
        title=_(u"Cover Image Caption"),
        required=False
    )

    fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['contact_email', 'time_slots', ]
    )
    contact_email = schema.TextLine(
        title=_(u"Recipient E-Mail"),
        required=True
    )
    time_slots = schema.List(
        title=u"Available Time Slots",
        description=u"Please enter available time slots that will be added to "
                    u"bookable consulting dates. Since the available time slots"
                    u" will automatically processed the entered values should"
                    u" adhere to the format: 14:00|14:15",
        required=False,
        value_type=schema.TextLine(
            title=_(u"Time Slot"),
        )
    )


@implementer(IConsultingSchedule)
class ConsultingSchedule(Container):
    pass
