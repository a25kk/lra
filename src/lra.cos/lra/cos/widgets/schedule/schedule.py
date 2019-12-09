# -*- coding: utf-8 -*-
"""Module providing site widget"""
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five import BrowserView
from ade25.base.interfaces import IContentInfoProvider
from ade25.widgets.interfaces import IContentWidgets

from future.backports import datetime
from lra.cos.interfaces import IConsultationSlotLocator
from plone import api
from zope.component import getUtility


class WidgetConsultationSchedule(BrowserView):
    """ Teaser widget for events """

    def __call__(self,
                 widget_name='lra-easer-events',
                 widget_type='lra-teaser-events',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    def has_content(self):
        if self.widget_has_data():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_data(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        return stored_widget

    @staticmethod
    def widget_display(public):
        if not public and api.user.is_anonymous():
            return False
        return True

    def widget_content(self):
        widget_content = self.widget_data()
        if widget_content:
            data = {
                'title': widget_content.get('title', None),
                'public': widget_content['is_public'],
                'display': self.widget_display(widget_content["is_public"])
            }
        else:
            data = {
                'title': None,
                'public': True,
                'display': True
            }
        return data

    def widget_content_items(self):
        return self.available_time_slots()

    def widget_custom_styles(self):
        if self.record and 'styles' in self.record:
            return self.record['styles']
        else:
            return None

    def widget_content_list_class(self):
        context = aq_inner(self.context)
        css_class = 'c-schedule__list c-schedule__list--default c-list--{}'.format(
            context.UID())
        custom_styles = self.widget_custom_styles()
        if custom_styles:
            class_container = custom_styles['class_container']
            for class_name in class_container.split(' '):
                css_class = '{0} c-schedule__list--{1}'.format(
                    css_class,
                    class_name
                )
            if 'custom' in custom_styles:
                css_class = '{0} {1}'.format(
                    css_class,
                    custom_styles['custom']
                )
        return css_class

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def widget_has_data(self):
        return len(self.stored_time_slots()) > 0

    @staticmethod
    def stored_time_slots():
        locator = getUtility(IConsultationSlotLocator)
        from_date = datetime.datetime.now()
        try:
            stored_slots = locator.available_slots(from_date)
            return stored_slots
        except:
            return list()

    def available_time_slots(self):
        context = aq_inner(self.context)
        stored_slots = self.stored_time_slots()
        available_slots = list()
        for time_slot in stored_slots:
            booking_url = "{0}/@@book-appointment/{1}".format(
                context.absolute_url(),
                time_slot["slot_code"]
            )
            time_slot.update({
                "slot_booking_url": booking_url,
                "slot_start": self.time_stamp(context, time_slot['slot_time']),
                "slot_end": self.time_stamp(context, time_slot['slot_time_end'])
            })
            available_slots.append(time_slot)
        return available_slots

    def recent_events(self):
        context = aq_inner(self.context)
        data = [
            {
                'uuid': '9b11d61b-d5e2-43a7-b372-2ab0c4f97e95',
                'css_classes': '',
                'bookable': False,
                'action_url': '{0}/@@book-appointment'.format(context.absolute_url()),
                'date': '17. Januar 2020',
                'day': 'Donnerstag',
                'start': '16:00',
                'end': '16:30'
             },
            {
                'uuid': '0a37fbbe-5344-48dd-9553-17ab3e774d03',
                'css_classes': '',
                'bookable': True,
                'action_url': '{0}/@@book-appointment'.format(context.absolute_url()),
                'date': '17. Januar 2020',
                'day': 'Donnerstag',
                'start': '16:45',
                'end': '17:15'
             },
        ]
        return data


class WidgetConsultationSlot(BrowserView):
    """ Teaser widget for events """

    def __call__(self,
                 widget_name='lra-consultation-slot',
                 widget_type='lra-consultation-slot',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    def has_content(self):
        if self.widget_has_data():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_data(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        return stored_widget

    @staticmethod
    def widget_display(public):
        if not public and api.user.is_anonymous():
            return False
        return True

    def widget_content(self):
        widget_content = self.widget_data()
        if widget_content:
            data = {
                'title': widget_content.get('title', None),
                'public': widget_content['is_public'],
                'display': self.widget_display(widget_content["is_public"])
            }
        else:
            data = {
                'title': None,
                'public': True,
                'display': True
            }
        return data

    def widget_custom_styles(self):
        if self.record and 'styles' in self.record:
            return self.record['styles']
        else:
            return None

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def widget_has_data(self):
        return len(self.get_latest_event_items()) > 0
