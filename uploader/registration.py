
class UploadHandlerList(object):
    """
    An UploadHandlerList object encapsulates an group of upload handler functions.
    mime types are registered with the UploadHandlerList using the register() method.
    """
    def __init__(self):
        self._registry = {}

    def register(self, mimetype, func):
        """
        Register a function to handle the file when a specific mimetype is uploaded.

        A list of mimetypes is also accepted
        """
        if not isinstance(mimetype, (list, tuple)):
            mimetype = [mimetype]

        for mtype in mimetype:
            self._registry[mtype] = func

    @property
    def acceptable_types(self):
        """
        Return the types acceptable for upload
        """
        from collections import defaultdict
        acceptable = defaultdict(list)
        if '*/*' in self._registry.keys():
            return {'All types': ['All']}
        for mtype in self._registry.keys():
            primary, secondary = mtype.split("/")
            if secondary == '*':
                acceptable[primary] = ['All']
            else:
                acceptable[primary].append(secondary)
        return acceptable

    def get_handler(self, mimetype):
        """
        Get the correct handler, allowing registered handlers to use:
        type/subtype, type/*, or */*
        """
        primary_type = "%s/*" % mimetype.split("/")[0]
        if mimetype in self._registry:
            return self._registry[mimetype]
        elif primary_type in self._registry:
            return self._registry[primary_type]
        elif '*/*' in self._registry:
            return self._registry['*/*']
        else:
            return None

upload_handlers = UploadHandlerList()


def autodiscover():
    try:
        from django.utils.module_loading import autodiscover_modules
    except ImportError:
        from .module_loading import autodiscover_modules

    autodiscover_modules('upload', register_to=upload_handlers)
