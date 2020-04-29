# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
import secrets
import json

from AccessControl import Unauthorized
from Acquisition import aq_inner
from ade25.base.interfaces import IContentInfoProvider
from ade25.base.mailer import send_mail, prepare_email_message, \
    create_plaintext_message, get_mail_template
from ade25.base.utils import encrypt_data_stream
from plone import api
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.component import getMultiAdapter, getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from lra.cos.appointments import ConsultationAppointment
from lra.cos.config import BOOKING_FORM
from lra.cos.interfaces import (AppointmentGenerationError,
                                IConsultationAppointmentGenerator,
                                IConsultationSlotLocator)

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
        required = self.form_fields_required_base()
        required_boolean = self.form_fields_required_boolean()
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
    def translate_value(token):
        return api.portal.translate(
            token,
            'lra.cos',
            api.portal.get_current_language())

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

    @staticmethod
    def _compose_message(data, template_name):
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        template_vars = {
            'email': data['email'],
            'subject': str(data['subject']),
            'message': data['comment'],
            'url': portal_url
        }
        template_name = template_name
        message = get_mail_template(template_name, template_vars)
        return message

    def prepare_booking_request(self, form_data):
        booking_request = dict()
        form_fields = self.form_fields()
        for field_id, field_details in form_fields.items():
            field_name = field_details.get("name")
            field_name_key = "{0}--title".format(field_id)
            booking_request.update({
                field_id: form_data.get(field_id, ""),
                field_name_key: self.translate_value(field_name)
            })
        return booking_request

    def send_confirmation_mail(self, mail_to, subject, form_data, template_name):
        email_subject = api.portal.translate(
            "Consulting on schedule: time slot appointment requested",
            'lra.cos',
            api.portal.get_current_language())
        mail_tpl = self._compose_message(form_data, template_name)
        mail_plain = create_plaintext_message(mail_tpl)
        msg = prepare_email_message(mail_tpl, mail_plain)
        recipients = [mail_to, ]
        send_mail(
            msg,
            recipients,
            subject
        )
        return

    def send_confirmation(self, form_data, appointment):
        context = aq_inner(self.context)
        email_from = api.portal.get_registry_record("plone.email_from_address")
        email_from_name = api.portal.get_registry_record("plone.email_from_name")
        contact_email = getattr(context, "contact_email", email_from)
        mail_to = form_data.get("email")
        mail_content = {
            "sender_name": email_from_name,
            "sender_email": contact_email,
            "appointment_code": appointment.get("consultationAppointmentCode"),
            "appointment_date": form_data.get("slot-date"),
            "appointment_time_slot": form_data.get("slot-time")
        }
        # mail_content.update(self.requested_time_slot())
        mail_content.update(self.prepare_booking_request(form_data))
        import pdb; pdb.set_trace()
        return

    def prepare_appointment_data(self, data):
        appointment = {
            "consultationAppointmentCode": secrets.token_urlsafe(64),
            "consultationAppointmentConstructionYear": data.get("construction_year"),
            "consultationAppointmentContactEmail": data.get("email"),
            "consultationAppointmentContactFirstName": data.get("first_name"),
            "consultationAppointmentContactLastName": data.get("last_name"),
            "consultationAppointmentContactSalutation": "",
            "consultationAppointmentRequest": encrypt_data_stream(
                json.dumps(data, ensure_ascii=False).encode('gbk')),
            "consultationSlotCode": self.slot_identifier,
            "data_protection_notice": True,
            "privacy_notice": True
        }
        return appointment

    def book_consultation_slot(self, data):
        context = aq_inner(self.context)
        generator = getUtility(IConsultationAppointmentGenerator)
        appointment = self.prepare_appointment_data(data)
        try:
            consultation_appointment = ConsultationAppointment(**appointment)
            generator(consultation_appointment)
        except AppointmentGenerationError as error:
            api.portal.show_message(
                str(error),
                self.request,
                type="error"
            )
        self.send_confirmation(data, appointment)
        next_url = '{0}/@@book-appointment-success/{1}'.format(
            context.absolute_url(),
            appointment.get("consultationAppointmentCode")
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

    @staticmethod
    def form_setup():
        return BOOKING_FORM

    def form_fields(self):
        fields = dict()
        for field_set in self.form_setup().values():
            for field in field_set.get("fields", list()):
                field_id = field.get("id")
                field.pop("id")
                fields.update({
                    field_id: field
                })
        return fields

    def form_fields_required(self):
        required_fields = {}
        for field_set in self.form_setup().values():
            for field in field_set.get("fields", list()):
                if field["required"]:
                    required_fields.update({field["id"]: field["field_type"]})
        return required_fields

    def form_fields_required_boolean(self):
        required = [
            form_field
            for form_field, field_type in self.form_fields_required().items()
            if field_type in ["boolean", "privacy"]
        ]
        return required

    def form_fields_required_base(self):
        required = [
            form_field
            for form_field, field_type in self.form_fields_required().items()
            if field_type not in ["boolean", "privacy"]
        ]
        return required

    def form_field_time_slot(self, time_only=False):
        time_slot = self.requested_time_slot()
        slot_start = time_slot.get("slot_start")
        slot_end = time_slot.get("slot_end")
        if time_only:
            field_value = "{start} - {end}".format(
                start=slot_start["time"],
                end=slot_end["time"],
            )
        else:
            field_value = "{day}. {month_name} {year}".format(
                day=slot_start["day"],
                month_name=slot_start["month_name"],
                year=slot_start["year"]
            )
        return field_value


@implementer(IPublishTraverse)
class BookAppointmentSuccess(BrowserView):

    appointment_identifier = None

    def publishTraverse(self, request, name):
        """When traversing to .../@@book-appointment-success/appointment-code,
        extract the necessary information and provide appropriate user feedback.
        """
        if self.appointment_identifier is None:
            self.appointment_identifier = name
            return self
        else:
            raise NotFound()
