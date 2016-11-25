# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility

from lra.sitecontent.interfaces import IResponsiveImagesTool


class BookableEventView(BrowserView):
    """ Bookable event default view """

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False
