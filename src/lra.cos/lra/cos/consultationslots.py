# -*- coding: utf-8 -*-
"""Module providing consultation slots"""
from sqlalchemy import types as sqlalchemy_types
from sqlalchemy import schema as sqlalchemy_schema
from zope import schema
from zope.interface import Interface, implements, implementer

from lra.cos import _, ORMBase


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

    def __init__(self):
        pass

    __tablename__ = 'screening'

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
    bookable = sqlalchemy_schema.Column(
        sqlalchemy_types.Boolean(),
        nullable=False,
    )

