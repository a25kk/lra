# -*- coding: utf-8 -*-
"""Module providing views for the site navigation root"""
from Products.Five.browser import BrowserView
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contenttypes.interfaces import INewsItem
from zope.component import getUtility

from lra.sitecontent.interfaces import IResponsiveImagesTool

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class FrontPageView(BrowserView):
    """ General purpose frontpage view """

    def __call__(self):
        self.has_newsitems = len(self.recent_news()) > 0
        return self.render()

    def render(self):
        return self.index()

    def can_edit(self):
        show = False
        if not api.user.is_anonymous():
            show = True
        return show

    def portal_id(self):
        portal = api.portal.get()
        return portal.id

    def recent_news(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=INewsItem.__identifier__,
                        review_state='published',
                        sort_on='Date',
                        sort_order='reverse',
                        sort_limit=3)[:3]
        return IContentListing(items)

    def section_preview(self, section):
        info = {}
        if section.startswith('/'):
            target = section
        else:
            target = '/{0}'.format(section)
        item = api.content.get(path=target)
        if item:
            info['title'] = item.Title()
            info['teaser'] = item.Description()
            info['url'] = item.absolute_url()
            info['image'] = self.image_tag(item)
            info['subitems'] = None
            if target in ('/news'):
                info['subitems'] = self.recent_news()
        return info

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)
