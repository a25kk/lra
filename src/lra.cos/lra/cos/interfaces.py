# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class ILRAConsultingOnSchedule(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IConsultationSlotLocator(Interface):
    """ Interface that defines a consultation slot lookup utility """


class IConsultationSlotGenerator(Interface):
    """ Interface that defines a consultation slot generator utility """


class IConsultationAppointmentLocator(Interface):
    """ Interface that defines a consultation appointment lookup utility """


class IConsultationAppointmentGenerator(Interface):
    """ Interface that defines a consultation appointment generator utility """


# Exceptions


class TimeSlotGenerationError(Exception):
    """Exception raised if there is an error generating bookable time slots
    """

class AppointmentGenerationError(Exception):
    """Exception raised if there is an error generating an appointment
    """
