# -*- coding: utf-8 -*-
"""Module providing an image scaling factory."""

from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest


class ResponsiveImagesTool(object):
    """ Factory providing rescaling of project images """

    def create(self, uuid):
        item = api.content.get(UID=uuid)
        data = self._get_image_data(item)
        return data

    def _get_image_data(self, item):
        data = {}
        sizes = ['small', 'medium', 'large', 'original']
        idx = 0
        for size in sizes:
            idx += 0
            img = self._get_scaled_img(item, size)
            data[size] = '{0} {1}w'.format(img['url'], img['width'])
        return data

    def _get_scaled_img(self, item, size):
        request = getRequest()
        if (
            ICatalogBrain.providedBy(item) or
            IContentListingObject.providedBy(item)
        ):
            obj = item.getObject()
        else:
            obj = item
        info = {}
        if hasattr(obj, 'image'):
            scales = getMultiAdapter((obj, request), name='images')
            if size == 'small':
                scale = scales.scale('image', width=300, height=300)
            if size == 'medium':
                scale = scales.scale('image', width=600, height=600)
            if size == 'large':
                scale = scales.scale('image', width=900, height=900)
            else:
                scale = scales.scale('image', width=1200, height=1200)
            if scale is not None:
                info['url'] = scale.url
                info['width'] = scale.width
                info['height'] = scale.height
            else:
                info['url'] = IMG
                info['width'] = '1px'
                info['height'] = '1px'
        else:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info
