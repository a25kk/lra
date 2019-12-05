# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
import datetime
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from lra.cos.consultationslots import ConsultationSlot
from lra.cos.interfaces import IConsultationSlotGenerator, TimeSlotGenerationError

from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from z3c.form import button, form
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from plone.app.z3cform.widget import DatetimeFieldWidget
from zope.schema.interfaces import IVocabularyFactory

from lra.cos import _


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def time_slot_date_default_value():
    today = datetime.datetime.today()
    next_thursday = next_weekday(today, 3)
    return next_thursday


def time_slot_dates_until_default_value():
    today = datetime.datetime.today()
    next_thursday = next_weekday(today, 3)
    return next_thursday + datetime.timedelta(7)


class ManageTimeSlots(BrowserView):
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
                "LRA Consultation Slots: Manage Slots", user=current_user, obj=context
            )
        return display_toolbar

    def rendered_widget(self):
        context = aq_inner(self.context)
        view_name = "@@content-widget-lra-consultation-schedule"
        rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget


class ITimeSlotAddForm(model.Schema):

    time_slot = schema.Datetime(
        title=_(u"Consultation Date"),
        description=_(u"Please enter a date for consultations on schedule"),
        required=True,
        defaultFactory=time_slot_date_default_value,
    )

    directives.widget("time_slot", DatetimeFieldWidget, pattern_options={"time": False})

    time_slots_until = schema.Datetime(
        title=_(u"Time Slot Creation Until (Optional)"),
        description=_(u"Please enter a future date for iterative creation"),
        required=False,
        defaultFactory=time_slot_dates_until_default_value,
    )

    directives.widget(
        "time_slots_until", DatetimeFieldWidget, pattern_options={"time": False}
    )


@implementer(IPublishTraverse)
class TimeSlotAddForm(AutoExtensibleForm, form.Form):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = ITimeSlotAddForm
    ignoreContext = True
    css_class = "o-form o-form--widget"

    label = _(u"Consultation time slots")
    enableCSRFProtection = True
    formErrorsMessage = _(u"There were errors.")

    submitted = False

    @property
    def action(self):
        """ Rewrite HTTP POST action.
#        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        return self.context.absolute_url() + "/@@create-time-slot-form"

    @property
    def next_url(self):
        context = aq_inner(self.context)
        url = "{0}/@@manage-time-slots".format(context.absolute_url())
        return url

    def configured_time_slots(self):
        context = aq_inner(self.context)
        time_slots = list()
        stored_time_slots = getattr(context, "time_slots", None)
        if stored_time_slots:
            for slot in stored_time_slots:
                slot_values = slot.split("|")
                time_slots.append({"start": slot_values[0], "end": slot_values[1]})
        return time_slots

    @staticmethod
    def _compose_time_slot_data(
        date_base, slot_hour, slot_minutes, slot_hour_end, slot_minutes_end
    ):
        slot = {
            "slot_code": str(uuid_tool.uuid4()),
            "slot_time": date_base.replace(
                hour=int(slot_hour), minute=int(slot_minutes), second=00
            ),
            "slot_time_end": date_base.replace(
                hour=int(slot_hour_end), minute=int(slot_minutes_end), second=00
            ),
            "bookable": True,
        }
        return slot

    def generate_time_slots(self, consultation_date):
        generated_time_slots = list()
        configured_slots = self.configured_time_slots()
        for desired_slot in configured_slots:
            # Iterate over configured desired time slots and generate
            # datetime objects
            try:
                slot_start = desired_slot["start"].split(":")
                slot_end = desired_slot["end"].split(":")
                slot_data = self._compose_time_slot_data(
                    consultation_date,
                    slot_start[0],
                    slot_start[1],
                    slot_end[0],
                    slot_end[1],
                )
                generated_time_slots.append(slot_data)
            except IndexError:
                # Some exception handler should be in place
                pass
        import pdb

        pdb.set_trace()
        return generated_time_slots

    def prepare_time_slots(self, data):
        time_slots = list()
        cycle_date = data["time_slot"]
        cycle_end = data["time_slots_until"]
        step = datetime.timedelta(days=7)
        days_in_cycle = list()
        while cycle_date <= cycle_end:
            days_in_cycle.append(cycle_date)
            cycle_date += step
        if days_in_cycle:
            # Generate time slots for all stored time slots
            for single_date in days_in_cycle:
                time_slots.append(self.generate_time_slots(single_date))
        return time_slots

    def applyChanges(self, data):
        context = aq_inner(self.context)
        generator = getUtility(IConsultationSlotGenerator)
        time_slots = self.prepare_time_slots(data)
        for time_slot in time_slots:
            consultation_slot = ConsultationSlot(
                consultationSlotId=time_slot["slot_id"],
                consultationSlotCode=time_slot["slot_code"],
                consultationSlotTime=time_slot["slot_time"],
                bookable=time_slot["bookable"],
            )
            try:
                generator(consultation_slot)
            except TimeSlotGenerationError as error:
                IStatusMessage(self.request).add(str(error), type="error")
        return self.request.response.redirect(self.next_url)

    @button.buttonAndHandler(_(u"cancel"), name="cancel")
    def handleCancel(self, action):
        self.status = _(u"The process has been cancelled.")
        return self.request.response.redirect(addTokenToUrl(self.next_url))

    @button.buttonAndHandler(_(u"Create"), name="create")
    def handleApply(self, action):
        request = self.request
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        if request.get("form.buttons.create", None):
            self.submitted = True
            self.applyChanges(data)
        self.status = "Thank you very much!"

    def updateActions(self):
        super(TimeSlotAddForm, self).updateActions()
        self.actions["cancel"].addClass(
            "c-button--default c-button--cancel c-button--panel"
        )
        self.actions["create"].addClass("c-button--primary")


class TimeSlotAdd(FormWrapper):

    form = TimeSlotAddForm

    def __call__(self, debug="off", **kw):
        self.params = {"debug_mode": debug}
        # self._update_panel_editor(self.params)
        self.update()
        return self.render()

    def configured_time_slots(self):
        context = aq_inner(self.context)
        time_slots = list()
        stored_time_slots = getattr(context, "time_slots", None)
        if stored_time_slots:
            for slot in stored_time_slots:
                slot_values = slot.split("|")
                time_slots.append({"start": slot_values[0], "end": slot_values[1]})
        return time_slots

    def weekday_name(self, weekday):
        context = aq_inner(self.context)
        vocabulary_name = "plone.app.vocabularies.Weekdays"
        factory = getUtility(IVocabularyFactory, vocabulary_name)
        vocabulary = factory(context)
        translation_service = api.portal.get_tool(name="translation_service")
        weekday_name = translation_service.translate(
            vocabulary.getTerm(weekday).title,
            "plone",
            target_language=api.portal.get_default_language(),
        )
        return weekday_name
