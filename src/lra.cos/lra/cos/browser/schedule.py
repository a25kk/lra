# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone import api
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


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


@implementer(IPublishTraverse)
class BookAppointment(BrowserView):

    errors = dict()
    slot_identifier = None

    def __call__(self, debug="off", **kw):
        self.params = {"debug_mode": debug}
        # self._update_panel_editor(self.params)
        self.update()
        return self.render()

    def render(self):
        return self.index()

    def update(self):
        self.errors = dict()
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('email', 'subject')
        required_boolean = ('privacy-policy-agreement', 'privacy-policy')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            error_idx = 0
            if self.privacy_policy_enabled():
                for field_name in required_boolean:
                    if not field_name in form:
                        form_errors[field_name] = self.required_field_error()
                        error_idx += 1
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        form_errors[value] = self.required_field_error()
                        error_idx += 1
                    else:
                        error = {
                            'active': False,
                            'msg': form[value]
                        }
                        form_errors[value] = error
            if error_idx > 0:
                self.errors = form_errors
            else:
                self.book_consultation_slot(form)

    def publishTraverse(self, request, name):
        """When traversing to .../cinema/@@screenings/filmcode, store the
        film code and return self; the next step will be to render the view,
        which can then use the code.
        """
        if self.slot_identifier is None:
            self.slot_identifier = name
            return self
        else:
            raise NotFound()

    def book_consultation_slot(self, data):
        pass
