# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from ade25.base.interfaces import IContentInfoProvider
from lra.cos.appointments import ConsultationAppointment
from lra.cos.interfaces import IConsultationSlotLocator, \
    IConsultationAppointmentGenerator, AppointmentGenerationError
from plone import api
from zExceptions import NotFound
from zope.component import getMultiAdapter, getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from lra.cos import _


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
    form_data = dict()
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
        required = ('firstname', 'lastname', 'email', 'subject')
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
                self.form_data = form_data
            else:
                self.book_consultation_slot(form)

    def publishTraverse(self, request, name):
        """When traversing to .../@@book-appointment/time-slot-code, store the
        film code and return self; the next step will be to render the view,
        which can then use the code.
        """
        if self.slot_identifier is None:
            self.slot_identifier = name
            return self
        else:
            raise NotFound()

    @staticmethod
    def default_value(error):
        value = ''
        if error['active'] is True:
            value = error['msg']
        return value

    def default_error(self, field_name):
        default_field_error = {'active': False, 'msg': ''}
        return self.errors.get(field_name, default_field_error)

    @staticmethod
    def required_field_error():
        translation_service = api.portal.get_tool(name="translation_service")
        error = {}
        error_msg = _(u"This field is required")
        error['active'] = True
        error['msg'] = translation_service.translate(
            error_msg,
            'lra.cos',
            target_language=api.portal.get_default_language()
        )
        return error

    def default_field_value(self, field_name):
        return getattr(self.request, field_name, None)

    def prepare_appointment_data(self, data):
        import pdb; pdb.set_trace()
        return data

    def book_consultation_slot(self, data):
        context = aq_inner(self.context)
        generator = getUtility(IConsultationAppointmentGenerator)
        appointment = self.prepare_appointment_data(data)
        try:
            generator(appointment)
        except AppointmentGenerationError as error:
            api.portal.show_message(
                str(error),
                self.request,
                type="error"
            )
        next_url = '{0}/@@appointment-booking'.format(
            context.absolute_url()
        )
        return self.request.response.redirect(next_url)

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def requested_time_slot(self):
        context = aq_inner(self.context)
        locator = getUtility(IConsultationSlotLocator)
        time_slot = locator.time_slot(self.slot_identifier)
        time_slot.update({
            "slot_start": self.time_stamp(context, time_slot['slot_time']),
            "slot_end": self.time_stamp(context, time_slot['slot_time_end'])
        })
        return time_slot
