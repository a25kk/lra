# -*- coding: utf-8 -*-
"""Module providing package configuration"""
from lra.cos import MessageFactory as _

BOOKING_FORM = {
    'personnel': {
        "legend": _(u"Personnel Information"),
        "fields": [
            {
                "field_type": "text-line",
                "id": "first_name",
                "name": _(u"First name"),
                "required": True,
                "class": "spacer",
                "options": None
             },
            {
                "field_type": "text-line",
                "id": "last_name",
                "name": _(u"Last name"),
                "required": True,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "street",
                "name": _(u"Street"),
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "postcode",
                "name": _(u"Postcode"),
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "city",
                "name": _(u"City"),
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "phone",
                "name": _(u"Phone"),
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "email",
                "name": _(u"Email"),
                "required": True,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "recommendation",
                "name": _(u"Recommendation"),
                "required": True,
                "class": "spacer",
                "options": None
            }
        ]
    },
    "details": {
        "legend": _(u"Please specify your booking request"),
        "fields": [
            {
                "field_type": "select",
                "id": "building_type",
                "name": _(u"Building Type"),
                "required": False,
                "class": "spacer",
                "options": {
                    "detached": _(u"Detached house"),
                    "semidetached": _(u"Semidetached house"),
                    "apartment": _(u"Apartment house"),
                }
            },
            {
                "field_type": "text-line",
                "id": "apartments",
                "name": _(u"Apartments"),
                "required": True,
                "class": "spacer",
                "options": None
            }
        ]
    }
}