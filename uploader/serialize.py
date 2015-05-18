# encoding: utf-8
import mimetypes
import re

from django.conf import settings


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize(instance, file_attr='uploaded_file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    mimetype = mimetypes.guess_type(obj.path)[0] or 'image/png'

    out = {
        'url': instance.admin_url,
        'type': mimetype,
        'extension': mimetype.split("/")[1],
        'size': obj.size,
        'adminUrl': instance.admin_url,
    }
    if hasattr(instance, 'related_object'):
        opts = instance.related_object._meta
        app_label = opts.app_label
        model_name = getattr(opts, 'module_name', None) or getattr(opts, 'model_name', None)
        out['name'] = "%s %s: %s" % (app_label, model_name, unicode(instance.related_object))
        if instance.thumbnail_attr:
            url = getattr(instance.related_object, instance.thumbnail_attr)
            if callable(url):
                out['thumbnailUrl'] = url()
            else:
                out['thumbnailUrl'] = url.url
    else:
        out['name'] = "No handler for this type"
        out['error'] = "No handler for this type"
        out['thumbnailUrl'] = '%suploader/img/missing-image.svg' % settings.STATIC_URL
    return out
