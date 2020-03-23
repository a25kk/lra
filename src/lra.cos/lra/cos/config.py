# -*- coding: utf-8 -*-
"""Module providing package configuration"""
from lra.cos import _

BOOKING_FORM = {
    'personnel': {
        "legend": _(u"Personnel Information"),
        "fields": [
            {
                "field_type": "text-line",
                "id": "first_name",
                "name": _(u"First name"),
                "help_text": None,
                "required": True,
                "class": "spacer",
                "options": None
             },
            {
                "field_type": "text-line",
                "id": "last_name",
                "name": _(u"Last name"),
                "help_text": None,
                "required": True,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "street",
                "name": _(u"Street"),
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "postcode",
                "name": _(u"Postcode"),
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "city",
                "name": _(u"City"),
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "phone",
                "name": _(u"Phone"),
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "email",
                "name": _(u"Email"),
                "help_text": None,
                "required": True,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "recommendation",
                "name": _(u"Recommendation"),
                "help_text": _(u"How did you hear about us?"),
                "required": False,
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
                "help_text": None,
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
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "construction_year",
                "name": _(u"Construction Year"),
                "help_text": _(u"In order to be able to prepare your personal "
                               u"consultation appointment in the best possible way, we "
                               u"need this information."),
                "required": True,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "living_space",
                "name": _(u"Living Space"),
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "residents",
                "name": _(u"Residents"),
                "help_text": _(u"How many people live permanently in the household?"),
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "boolean",
                "id": "non_residential_building",
                "name": _(u"Non Residential Building"),
                "help_text": None,
                "required": False,
                "default": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-line",
                "id": "utilization",
                "name": _(u"Utilization"),
                "help_text": None,
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "text-area",
                "id": "comment",
                "name": _(u"Comment"),
                "help_text": _(u"Which topic is your main concern for a personal "
                               u"consultation?"),
                "required": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "boolean",
                "id": "privacy-policy",
                "name": _(u"By sending this message, I confirm that my details are "
                          u"correct and I agree to the collection and further "
                          u"processing of the provided data. The data will only be "
                          u"used for the purpose stated in your inquiry."),
                "help_text": None,
                "required": True,
                "default": False,
                "class": "spacer",
                "options": None
            },
            {
                "field_type": "privacy",
                "id": "privacy-agreement",
                "name": _(u"Privacy Agreement"),
                "help_text": {
                    "help_text_prefix": _(u"I have acknowledged the "),
                    "help_text_link": _(u"privacy policy"),
                    "help_text_link_url": "/rechtliche-hinweise",
                    "help_text_postfix": _(u"and accept it."),
                },
                "required": True,
                "default": False,
                "class": "spacer",
                "options": None
            }
        ]
    }
}