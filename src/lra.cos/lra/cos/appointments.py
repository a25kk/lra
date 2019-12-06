# -*- coding: utf-8 -*-
"""Module providing consultation appointment model"""
from lra.cos.interfaces import IConsultationAppointmentLocator, \
    IConsultationAppointmentGenerator
from sqlalchemy import Table
from sqlalchemy import schema as sqlalchemy_schema
from sqlalchemy import types as sqlalchemy_types
from z3c.saconfig import Session
from zope import schema
from zope.interface import Interface, implementer

from lra.cos import ORMBase
from lra.cos import _

metadata = ORMBase.metadata


class IConsultationAppointment(Interface):
    """ A consultation appointment """

    consultationAppointmentId = schema.Int(
        title=_(u"Consultation appointment identifier"),
    )

    consultationAppointmentCode = schema.TextLine(
        title=_(u"Consultation appointment code"),
    )

    consultationSlotCode = schema.TextLine(
        title=_(u"Consultation slot code"),
    )

    consultationAppointmentTimeStamp = schema.Datetime(
        title=_(u"Consultation appointment generated time stamp"),
    )

    privacy_notice = schema.Bool(
        title=_(u"Privacy notice accepted?"),
    )

    data_protection_notice = schema.Bool(
        title=_(u"Date protection notice accepted?"),
    )

    consultationAppointmentContactEmail = schema.TextLine(
        title=_(u"Consultation contact email"),
    )

    consultationAppointmentContactSalutation = schema.TextLine(
        title=_(u"Consultation contact salutation"),
    )

    consultationAppointmentContactFirstName = schema.TextLine(
        title=_(u"Consultation contact first name"),
    )

    consultationAppointmentContactLastName = schema.TextLine(
        title=_(u"Consultation contact last name"),
    )

    consultationAppointmentConstructionYear = schema.TextLine(
        title=_(u"Consultation appointment construction year"),
    )

    consultationAppointmentRequest = schema.Text(
        title=_(u"Consultation appointment request"),
    )


@implementer(IConsultationAppointment)
class ConsultationAppointment(ORMBase):
    """ Database-backed implementation of IConsultationAppointment """

    __tablename__ = 'consultation_appointment'

    consultationAppointmentId = sqlalchemy_schema.Column(
        sqlalchemy_types.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    # Generated via secrets.token_hex
    consultationAppointmentCode = sqlalchemy_schema.Column(
        sqlalchemy_types.String(64),
        nullable=False,
    )

    # Generated via secrets.token_hex
    consultationSlotCode = sqlalchemy_schema.Column(
        sqlalchemy_types.String(64),
        nullable=False,
    )

    consultationAppointmentTimeStamp = sqlalchemy_schema.Column(
        sqlalchemy_types.DateTime(),
        nullable=False,
    )

    privacy_notice = sqlalchemy_schema.Column(
        sqlalchemy_types.Boolean(),
        nullable=False,
    )

    data_protection_notice = sqlalchemy_schema.Column(
        sqlalchemy_types.Boolean(),
        nullable=False,
    )

    consultationAppointmentContactEmail = sqlalchemy_schema.Column(
        sqlalchemy_types.String(120),
        nullable=False,
    )

    consultationAppointmentContactSalutation = sqlalchemy_schema.Column(
        sqlalchemy_types.String(120),
        nullable=False,
    )

    consultationAppointmentContactFirstName = sqlalchemy_schema.Column(
        sqlalchemy_types.String(120),
        nullable=False,
    )

    consultationAppointmentContactLastName = sqlalchemy_schema.Column(
        sqlalchemy_types.String(120),
        nullable=False,
    )

    consultationAppointmentConstructionYear = sqlalchemy_schema.Column(
        sqlalchemy_types.String(64),
        nullable=False,
    )

    consultationAppointmentRequest = sqlalchemy_schema.Column(
        sqlalchemy_types.Text(),
        nullable=False,
    )


consultation_appointment = Table('consultation_appointment', metadata)


@implementer(IConsultationAppointmentLocator)
class ConsultationAppointmentLocator(object):
    """ Utility to locate available consultation slots """

    @staticmethod
    def available_slots(from_date):
        """Return a list of all films showing at the particular cinema
        between the specified dates.

        Returns a list of dictionaries with keys 'filmCode', 'url', 'title'
        and 'summary'.
        """

        results = Session.query(ConsultationAppointment).filter(
            ConsultationAppointment.showTime.after(from_date)
        )

        slots = [dict(appointment_id=row.consutationAppointmentId,
                      consultation_slot_code=row.consultationSlotCode,
                      appointment_code=row.consultationAppointmentCode,
                      appointment_email=row.consultationAppointmentContactEmail
                      )
                 for row in results]
        return slots


@implementer(IConsultationAppointmentGenerator)
class ConsultationAppointmentGenerator(object):
    """ Utility to generate new consultation slots """

    def __call__(self, appointment_request):
        """Make a consultation appointment
        """

        # Make sure the time slot is still available
        # TODO: check for data validity
        Session.add(appointment_request)
