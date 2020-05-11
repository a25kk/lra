# -*- coding: utf-8 -*-
"""Init and utils."""
from sqlalchemy.ext import declarative
from z3c.saconfig import named_scoped_session
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('lra.cos')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


# Create a base class used for object relational mapping classes
ORMBase = declarative.declarative_base()
Session = named_scoped_session('lra_cos')
