# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api


class ConsultingScheduleView(BrowserView):
    """ Consulting schedule view """

    @staticmethod
    def is_editable():
        editable = False
        if not api.user.is_anonymous():
            editable = True
        return editable

    def show_toolbar(self):
        context = aq_inner(self.context)
        display_toolbar = False
        if self.is_editable():
            # Explicitly check for permissions
            current_user = api.user.get_current()
            display_toolbar = api.user.has_permission(
                'LRA Consultation Slots: Manage Slots',
                user=current_user,
                obj=context
            )
        return display_toolbar

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def rendered_widget(self):
        context = aq_inner(self.context)
        view_name = '@@content-widget-lra-consultation-schedule'
        rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget
