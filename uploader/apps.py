from django.apps import AppConfig


class UploaderConfig(AppConfig):
    name = 'uploader'

    def ready(self):
        from .registration import autodiscover, upload_handlers  # NOQA
        autodiscover()
