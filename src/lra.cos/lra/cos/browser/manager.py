# -*- coding: utf-8 -*-
"""Module providing views for consulting schedules """
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import form
from zope import schema

from lra.cos import _
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


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
                'LRA Consultation Slots: Manage Slots',
                user=current_user,
                obj=context
            )
        return display_toolbar

    def rendered_widget(self):
        context = aq_inner(self.context)
        view_name = '@@content-widget-lra-consultation-schedule'
        rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget


class ITimeSlotAddForm(model.Schema):

    time_slot = schema.Datetime(
        title=_(u"Consultation Date"),
        description=_(u"Please enter a date for consultations on schedule. "
                      u"The corresponding time slots are added by the system."),
        required=True
    )


@implementer(IPublishTraverse)
class TimeSlotAddForm(AutoExtensibleForm, form.Form):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = ITimeSlotAddForm
    ignoreContext = False
    css_class = 'o-form o-form--widget'

    label = _(u'Consultation time slots')
    enableCSRFProtection = True
    formErrorsMessage = _(u'There were errors.')

    submitted = False

    @property
    def action(self):
        """ Rewrite HTTP POST action.
#        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        return self.context.absolute_url() + "/@@content-widget-item-form"

    def applyChanges(self, data):
        context = aq_inner(self.context)
        next_url = '{url}/@@panel-edit?section={section}&panel={panel}'.format(
            url=context.absolute_url(),
            section=editor_data["content_section"],
            panel=editor_data["content_section_panel"]
        )
        return self.request.response.redirect(next_url)

    @button.buttonAndHandler(_(u'cancel'), name='cancel')
    def handleCancel(self, action):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        next_url = '{url}/@@panel-edit?section={section}&panel={panel}'.format(
            url=context.absolute_url(),
            section=editor_data["content_section"],
            panel=editor_data["content_section_panel"]
        )
        return self.request.response.redirect(addTokenToUrl(next_url))

    @button.buttonAndHandler(_(u'Create'), name='create')
    def handleApply(self, action):
        request = self.request
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        if request.get('form.buttons.update', None):
            self.submitted = True
            self.applyChanges(data)
        self.status = "Thank you very much!"

    def updateActions(self):
        super(TimeSlotAddForm, self).updateActions()
        self.actions["cancel"].addClass(
            "c-button--default c-button--cancel c-button--panel")
        self.actions["create"].addClass("c-button--primary")


class TimeSlotAdd(FormWrapper):

    form = TimeSlotAddForm

    def __call__(self,
                 debug='off',
                 **kw):
        self.params = {
            'debug_mode': debug
        }
        # self._update_panel_editor(self.params)
        self.update()
        return self.render()
