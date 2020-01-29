# -*- coding: utf-8 -*-
"""Module providing custom content listing"""
from Acquisition import aq_inner
from Products.Five import BrowserView
from plone import api


class CustomContentListing(BrowserView):

    def __call__(self):
        self.has_content = len(self.contained_items()) > 0
        return self.render()

    def render(self):
        return self.index()

    def panel_page_support_enabled(self):
        context = aq_inner(self.context)
        try:
            from ade25.panelpage.behaviors.storage import IContentPanelStorage
            if IContentPanelStorage.providedBy(context):
                return True
            else:
                return False
        except ImportError:
            return False

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def content_items(self):
        results = []
        brains = self.contained_items()
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'timestamp': brain.Date,
                'uuid': brain.UID,
                'item_object': brain.getObject()
            })
        return results

    def contained_items(self):
        container = aq_inner(self.context)
        items = api.content.find(
            context=container,
            depth=1,
            portal_type=[
                'lra.sitecontent.sectionfolder',
                'lra.sitecontent.contentpage',
                'News Item',
                'Event',
                'Folder'
            ],
            review_state='published',
            sort_on='Date',
            sort_order='reverse'
        )
        return items

