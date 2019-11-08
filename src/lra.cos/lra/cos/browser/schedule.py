# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api


class ConsultingScheduleView(BrowserView):
    """ Consulting schedule view """

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False
