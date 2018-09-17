# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
import datetime
import pytz
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter
from zope.component import getUtility

from lra.sitecontent.mailer import create_plaintext_message
from lra.sitecontent.mailer import prepare_email_message
from lra.sitecontent.mailer import get_mail_template
from lra.sitecontent.mailer import send_mail

from lra.sitecontent.interfaces import IResponsiveImagesTool

from lra.sitecontent import _


class BookableEventView(BrowserView):
    """ Bookable event default view """

    def __call__(self):
        self.errors = {}
        return self.render()

    def update(self):
        translation_service = api.portal.get_tool(name="translation_service")
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('email', 'fullname', 'phone')
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
                self.send_inquiry(form)

    def render(self):
        self.update()
        return self.index()

    def is_open_for_registration(self):
        context = aq_inner(self.context)
        start_date = getattr(context, 'start', None)
        if start_date:
            utc = pytz.UTC
            timezone_aware_start = start_date.replace(tzinfo=utc)
            now = utc.localize(datetime.datetime.now())
            if timezone_aware_start > now:
                return True
        return False

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value

    @staticmethod
    def required_field_error():
        translation_service = api.portal.get_tool(name="translation_service")
        error = {}
        error_msg = _(u"This field is required")
        error['active'] = True
        error['msg'] = translation_service.translate(
            error_msg,
            'ade25.contacts',
            target_language=api.portal.get_default_language()
        )
        return error

    @staticmethod
    def privacy_policy_enabled():
        try:
            enabled = api.portal.get_registry_record(
                name='ade25.contacts.display_privacy_policy'
            )
        except InvalidParameterError:
            enabled = False
        if enabled:
            return enabled
        return False

    @staticmethod
    def privacy_policy_url():
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        policy_url = api.portal.get_registry_record(
            name='ade25.contacts.privacy_policy_url'
        )
        if policy_url:
            url = '{0}{1}'.format(portal_url, policy_url)
            return url
        else:
            url = '{0}/datenschutzbestimmung'.format(portal_url)
            return url

    def _compose_message(self, data):
        context = aq_inner(self.context)
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        plone_tool = getMultiAdapter((context, self.request), name="plone")
        event_date = plone_tool.toLocalizedTime(context.start, long_format=True)
        template_vars = {
            'email': data['email'],
            'subject': str(data['subject']),
            'fullname': data['fullname'],
            'phone': data['phone'],
            'url': portal_url,
            'event': context.Title(),
            'privacy': data['privacy-policy'],
            'privacy-agreement': data['privacy-policy-agreement'],
            'date': '{0} Uhr'.format(str(event_date))
        }
        template_name = 'bookable-event-mail.html'
        message = get_mail_template(template_name, template_vars)
        return message

    def send_inquiry(self, data):
        context = aq_inner(self.context)
        subject = _(u"Inquiry from website visitor")  # noqa
        email_subject = api.portal.translate(
            "Inquiry from website visitor",
            'lra.sitecontent',
            api.portal.get_current_language())
        data['subject'] = email_subject
        mail_tpl = self._compose_message(data)
        mail_plain = create_plaintext_message(mail_tpl)
        msg = prepare_email_message(mail_tpl, mail_plain)
        default_email = api.portal.get_registry_record(
            'plone.email_from_address')
        recipient_email = data['email']
        registration_email = getattr(context, 'contact_email', default_email)
        recipients = [recipient_email, registration_email]
        send_mail(
            msg,
            recipients,
            email_subject
        )
        next_url = '{0}/@@bookable-event-dispatched'.format(
            context.absolute_url()
        )
        return self.request.response.redirect(next_url)

    def has_rich_text(self):
        context = aq_inner(self.context)
        try:
            rich_text = context.text
        except AttributeError:
            rich_text = None
        if rich_text is not None:
            return True
        return False

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)


class BookableEventFormDispatchedView(BrowserView):
    """ Inquiry form dispatched

        Show thank you page with feedback on how and when the request
        was processed
    """

    def processed_timestamp(self):
        datetime_now = datetime.datetime.utcnow()
        now = datetime_now.replace(tzinfo=pytz.utc)
        timestamp_data = {
            'date': api.portal.get_localized_time(now),
            'time': api.portal.get_localized_time(now, time_only=True),
        }
        return timestamp_data
