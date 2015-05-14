# -*- coding: utf-8 -*-
from django.conf import settings as site_settings


DEFAULT_SETTINGS = {
    'STORAGE_CLASS': None,  # What class to use to store the files
    'MEDIA_PREFIX': 'uploader/',  # Where the file uploader files are located
    'JQUERY_URL': '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(site_settings, 'uploader_SETTINGS', {}))

globals().update(USER_SETTINGS)
