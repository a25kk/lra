# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from zope.interface import implementer

from lra.sitecontent import _


class IContentPage(model.Schema, IImageScaleTraversable):
    """
    A container based content page
    """
    displayFileList = schema.Bool(
        title=_(u"Check to enable file listing"),
        description=_(u"When activated the view will attempt to display an "
                      u"automatic listing of all contained files with "
                      u"file information and download link."),
        required=False,
    )


@implementer(IContentPage)
class ContentPage(Container):
    pass
