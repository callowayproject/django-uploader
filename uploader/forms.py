# -*- coding: utf-8 -*-
from django import forms
from settings import MEDIA_PREFIX
from .models import Upload

"""
JS Docs

jquery.fileupload.js
    The basic File Upload plugin

jquery.iframe-transport.js
    The Iframe Transport is required for browsers without support for XHR file uploads

jquery.ui.widget.js
    The jQuery UI widget factory, can be omitted if jQuery UI is already included

jquery.cookie.js
    This plugin simplifies the passing of the CSRF token via AJAX

jquery.fileupload-process.js
    The File Upload processing plugin

jquery.fileupload-image.js
    The File Upload image preview & resize plugin

jquery.fileupload-audio.js
    The File Upload audio preview plugin

jquery.fileupload-video.js
    The File Upload video preview plugin

jquery.fileupload-validate.js
    The File Upload validation plugin

jquery.fileupload-ui.js
    The File Upload user interface plugin

"""


def prefix(string_or_list):
    if isinstance(string_or_list, list):
        return ['%s%s' % (MEDIA_PREFIX, x) for x in string_or_list]
    elif isinstance(string_or_list, tuple):
        return tuple(['%s%s' % (MEDIA_PREFIX, x) for x in string_or_list])
    elif isinstance(string_or_list, basestring):
        return '%s%s' % (MEDIA_PREFIX, string_or_list)
    return string_or_list


class BaseUploadForm(forms.ModelForm):
    """
    The basic form without media.
    """
    uploaded_file = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': 'true'}))

    class Meta:
        model = Upload
        fields = ('uploaded_file', )

    def clean(self):
        import mimetypes
        from .registration import upload_handlers

        data = self.cleaned_data['uploaded_file']
        mtype = mimetypes.guess_type(data.name)[0]
        if upload_handlers.get_handler(mtype) is None:
            raise forms.ValidationError("There is not a registered handler for %(mimetype)s files.",
                code='invalid',
                params={'mimetype': mtype}
            )


class BasicUploadForm(BaseUploadForm):
    """
    Form with just the basic upload script
    """
    class Media:
        css = {
            'all': prefix((
                'css/jquery.fileupload-ui.css',
                'css/jquery.fileupload-ui-noscript.css',
                'css/fileicon.css',
            )),
        }
        js = prefix((
            "js/jquery.ui.widget.js",
            "js/jquery.iframe-transport.js",
            "js/jquery.fileupload.js",
            "js/jquery.cookie.js",
        ))


class AdvancedUploadForm(BaseUploadForm):
    """
    Form with all the bells and whistles
    """
    class Media:
        css = {
            'all': prefix((
                'css/jquery.fileupload-ui.css',
                'css/fileicon.css',
            )),
        }
        js = prefix((
            "js/uploader.js",
            "js/locale.js",
        ))
