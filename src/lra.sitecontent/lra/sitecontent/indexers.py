# -*- coding: utf-8 -*-
"""Module providing a custom indexing setup for site content"""
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.textfield.value import IRichTextValue
from plone.indexer.decorator import indexer

from lra.sitecontent.contentpage import IContentPage
from lra.sitecontent.sectionfolder import ISectionFolder


def _unicode_save_string_concat(*args):
    """ Concat args and return utf-8 strings
        Operates independent of input format (unicode or str)
    """
    result = ''
    for value in args:
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'replace')
        result = ' '.join((result, value))
    return result


def SearchableText(obj):
    text = u""
    rich_text = IRichText(obj, None)
    if rich_text:
        text_value = rich_text.text
        if IRichTextValue.providedBy(text_value):
            transforms = getToolByName(obj, 'portal_transforms')
            text = transforms.convertTo(
                'text/plain',
                safe_unicode(text_value.output).encode('utf8'),
                mimetype=text_value.mimeType,
            ).getData().strip()

    subject = u' '.join(
        [safe_unicode(s) for s in obj.Subject()]
    )

    return u" ".join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u"",
        safe_unicode(obj.description) or u"",
        safe_unicode(text),
        safe_unicode(subject),
    ))


@indexer(IContentPage)
def searchable_text_content_page(obj):
    return _unicode_save_string_concat(SearchableText(obj))


@indexer(ISectionFolder)
def searchable_text_section_folder(obj):
    return _unicode_save_string_concat(SearchableText(obj))
