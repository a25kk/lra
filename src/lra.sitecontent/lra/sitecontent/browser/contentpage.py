# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api

from Products.MimetypesRegistry.MimeTypeItem import guess_icon_path
from zope.component import getMultiAdapter
from zope.component import getUtility

from lra.sitecontent.interfaces import IResponsiveImagesTool

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class ContentPageView(BrowserView):
    """ Folderish content page default view """

    def has_leadimage(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def display_file_list(self):
        context = aq_inner(self.context)
        try:
            display = context.displayFileList
        except AttributeError:
            display = None
        if display is not None:
            return display
        return False

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)

    def rendered_file_list(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@file-list')()
        return template


class GalleryPreview(BrowserView):
    """Preview embeddable image gallery"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def rendered_gallery(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@gallery-view')()
        return template


class GalleryView(BrowserView):
    """Provide gallery of contained image content"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def has_leadimage(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def leadimage_tag(self):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item

    def contained_images(self):
        context = aq_inner(self.context)
        data = context.restrictedTraverse('@@folderListing')(
            portal_type='Image',
            sort_on='getObjPositionInParent')
        return data

    def image_tag(self, image):
        context = image.getObject()
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item

    def _get_scaled_img(self, size):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        if size == 'small':
            scale = scales.scale('image', width=300, height=300)
        if size == 'medium':
            scale = scales.scale('image', width=600, height=600)
        else:
            scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item


class FileListPreview(BrowserView):
    """Preview embeddable image gallery"""

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def rendered_file_list(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@file-list')()
        return template


class FileListView(BrowserView):

    def __call__(self):
        self.has_assets = len(self.contained_files()) > 0
        return self.render()

    def render(self):
        return self.index()

    def contained_files(self):
        context = aq_inner(self.context)
        data = context.restrictedTraverse('@@folderListing')(
            portal_type='File',
            sort_on='getObjPositionInParent')
        return data

    def get_file_details(self, content_file):
        file_object = api.content.get(UID=content_file.UID)
        attachment = getattr(file_object, 'file', None)
        file_url = file_object.absolute_url()
        file_name = attachment.filename
        if attachment:
            details = {
                'file_name': file_name,
                'file_url': file_url,
                'is_video_type': self.is_video_type(attachment),
                'is_audio_type': self.is_video_type(attachment),
                'mime_icon': self.get_mime_type_icon(attachment),
                'file_size': attachment.getSize() / 1024,
                'content_type': getattr(
                    attachment, 'contentType', 'application/octet-stream'),
            }
        return details

    @staticmethod
    def is_video_type(content_file):
        ct = content_file.contentType
        return 'video/' in ct

    @staticmethod
    def is_audio_type(content_file):
        ct = content_file.contentType
        return 'audio/' in ct

    @staticmethod
    def get_mime_type_icon(content_file):
        portal_url = api.portal.get().absolute_url()
        mtr = api.portal.get_tool("mimetypes_registry")
        mime = []
        if content_file.contentType:
            mime.append(mtr.lookup(content_file.contentType))
        if content_file.filename:
            mime.append(mtr.lookupExtension(content_file.filename))
        mime.append(mtr.lookup("application/octet-stream")[0])
        icon_paths = [m.icon_path for m in mime if hasattr(m, 'icon_path')]
        if icon_paths:
            return icon_paths[0]

        return portal_url + "/" + guess_icon_path(mime[0])