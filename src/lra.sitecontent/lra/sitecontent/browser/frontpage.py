# -*- coding: utf-8 -*-
"""Module providing views for the site navigation root"""
from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from ade25.banner.contentbanner import IContentBanner
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.contenttypes.interfaces import INewsItem
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
from zope.component import getUtility

from lra.sitecontent.interfaces import IResponsiveImagesTool

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='
BG = 'background:url({0}) no-repeat 50% 0 transparent;'


class LandingPageView(BrowserView):
    """ Landing page

    Dedicated view to hold a live search and potential introduction
    """


class FrontPageView(BrowserView):
    """ General purpose frontpage view """

    def __call__(self):
        self.has_newsitems = len(self.recent_news()) > 0
        self.has_banners = len(self.banners()) > 0
        self.show_carousel = len(self.banners()) > 1
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

    def static_banner(self):
        items = self.banners()
        first_item = items[0].getObject()
        return IUUID(first_item, None)

    @staticmethod
    def render_item(uid):
        item = api.content.get(UID=uid)
        # template = item.restrictedTraverse('@@banner-view')()
        template = '<div class="c-alert c-alert--default">{0}</div>'.format(
            uid
        )
        return template

    def get_banner_image(self, banner):
        context = banner
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image')
        if scale is not None:
            image_tag = scale.url
        else:
            image_tag = IMG
        return image_tag

    def banner_background(self, banner):
        img = self.get_banner_image(banner)
        alt = BG.format(img)
        # style = 'background: transparent'
        style = alt
        if self.is_first_banner(banner):
            style = alt
        return style

    def is_first_banner(self, banner):
        context = banner
        first_item = self.banners()[0]
        primary = False
        if first_item.UID == IUUID(banner):
            primary = True
        return primary

    @staticmethod
    def has_data(banner):
        context = banner
        has_content = False
        if banner.headline or banner.text or banner.Description():
            has_content = True
        return has_content

    @staticmethod
    def has_link_action(banner):
        context = banner
        if context.link:
            return True
        return False

    @staticmethod
    def get_link_action(banner):
        context = banner
        link = context.link
        link_action = replace_link_variables_by_paths(context, link)
        return link_action

    def banners(self):
        context = aq_inner(self.context)
        parent = aq_parent(self.context)
        context_state = getMultiAdapter(
            (context, self.request), name=u'plone_context_state')
        if context_state.is_default_page() and INavigationRoot.providedBy(
                parent):
            assignment_context = parent
        else:
            assignment_context = context
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=IContentBanner.__identifier__,
                        path=dict(query='/'.join(
                            assignment_context.getPhysicalPath()
                        ),
                            depth=1),
                        review_state='published',
                        sort_on='getObjPositionInParent')
        return items

    def content_banners(self):
        content_banners = list()
        base_class = 'app-banner-item app-banner-item-lazy lazyload app-banner__item--lazy'  # noqa
        for brain in self.banners():
            banner_obj = brain.getObject()
            banner_data = {
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'timestamp': brain.Date,
                'uuid': brain.UID,
                "css_classes": "{0} app-banner__item--{1}{2}".format(
                    base_class,
                    brain.UID,
                    self.is_first_banner(banner_obj) and ' active' or ''
                ),
                'is_first': self.is_first_banner(banner_obj),
                'has_data': self.has_data(banner_obj),
                'has_link': self.has_link_action(banner_obj),
                'link': self.get_link_action(banner_obj),
                'img': self.get_banner_image(banner_obj),
                'bg_img': self.banner_background(banner_obj),
                'headline': getattr(banner_obj, 'headline', None),
                'text': getattr(banner_obj, 'text', None)
            }
            content_banners.append(banner_data)
        return content_banners

    @staticmethod
    def get_latest_news_items(limit=3):
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=INewsItem.__identifier__,
                        review_state='published',
                        sort_on='Date',
                        sort_order='reverse',
                        sort_limit=limit)[:limit]
        return items

    def recent_news(self):
        results = []
        brains = self.get_latest_news_items()
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'timestamp': brain.Date,
                'uuid': brain.UID,
                "css_classes": "o-card-list__item--{0}".format(
                    brain.UID
                ),
                'item_object': brain.getObject()
            })
        return results

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

    def image_tag(self, item):
        data = {}
        sizes = ['small', 'medium', 'large']
        idx = 0
        for size in sizes:
            idx += 0
            img = self._get_scaled_img(item, size)
            data[size] = '{0} {1}w'.format(img['url'], img['width'])
        return data

    def _get_scaled_img(self, item, size):
        if (
            ICatalogBrain.providedBy(item) or
            IContentListingObject.providedBy(item)
        ):
            obj = item.getObject()
        else:
            obj = item
        info = {}
        if hasattr(obj, 'image'):
            scales = getMultiAdapter((obj, self.request), name='images')
            if size == 'small':
                scale = scales.scale('image', width=300, height=300)
            if size == 'medium':
                scale = scales.scale('image', width=600, height=600)
            else:
                scale = scales.scale('image', width=900, height=900)
            if scale is not None:
                info['url'] = scale.url
                info['width'] = scale.width
                info['height'] = scale.height
        else:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info
