# -*- coding: utf-8 -*-
"""Module providing consultation slots"""
from sqlalchemy import Table
from sqlalchemy import schema as sqlalchemy_schema
from sqlalchemy import types as sqlalchemy_types
from z3c.saconfig import Session
from zope import schema
from zope.interface import Interface, implementer, implements

from lra.cos import ORMBase
from lra.cos.interfaces import (IConsultationSlotGenerator,
                                IConsultationSlotLocator)

from lra.cos import _

metadata = ORMBase.metadata


class IConsultationSlot(Interface):
    """A bookable consultation slot
    """

    consultationSlotId = schema.Int(
        title=_(u"Consultation slot identifier"),
    )

    consultationSlotCode = schema.TextLine(
        title=_(u"Consultation slot code"),
    )

    consultationSlotTime = schema.Datetime(
        title=_(u"Consultation slot time"),
    )

    bookable = schema.Bool(
        title=_(u"Is this slot still bookable?"),
    )


@implementer(IConsultationSlot)
class ConsultationSlot(ORMBase):
    """Database-backed implementation of IScreening
    """

    __tablename__ = 'consultation_slots'

    consultationSlotId = sqlalchemy_schema.Column(
        sqlalchemy_types.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    # Generated via secrets.token_hex
    consultationSlotCode = sqlalchemy_schema.Column(
        sqlalchemy_types.String(64),
        nullable=False,
    )

    consultationSlotTime = sqlalchemy_schema.Column(
        sqlalchemy_types.DateTime(),
        nullable=False,
    )

    consultationSlotTimeEnd = sqlalchemy_schema.Column(
        sqlalchemy_types.DateTime(),
        nullable=False,
    )

    bookable = sqlalchemy_schema.Column(
        sqlalchemy_types.Boolean(),
        nullable=False,
    )


consultation_slot = Table('consultation_slots', metadata)


@implementer(IConsultationSlotLocator)
class ConsultationSlotLocator(object):
    """ Utility to locate available consultation slots """

    @staticmethod
    def available_slots(from_date):
        """Return a list of all films showing at the particular cinema
        between the specified dates.

        Returns a list of dictionaries with keys 'filmCode', 'url', 'title'
        and 'summary'.
        """

        results = Session.query(ConsultationSlot).filter(
            ConsultationSlot.consultationSlotTime.after(from_date)
        )

        slots = [dict(slot_id=row.consutationSlotId,
                      slot_code=row.consultationSlotCode,
                      slot_time=row.consultationSlotTime,
                      slot_time_end=row.consultationSlotTimeEnd,
                      bookable=row.bookable
                      )
                 for row in results]
        return slots


@implementer(IConsultationSlotGenerator)
class ConsultationSlotGenerator(object):
    """ Utility to generate new consultation slots """

    def __call__(self, time_slot):
        """Make a time slot entry
        """

        # Make sure there are still seats available
        # TODO: check for data validity
        Session.add(time_slot)
