***************
Django Uploader
***************


What it does
============

Django Uploader uses `jQuery file upload`_ to allow drag-and-drop file upload of any file type in the Django Admin. Third-party applications to write handlers for specific file types, and register them with Django Uploader. When a file of that type is uploaded, it passes the information to the handler so that it can make a new record with that file.

.. _jQuery file upload: https://blueimp.github.io/jQuery-File-Upload/



Installation
============

1. Installation is easy using ``pip``::

   pip install django-uploader

2. Add ``uploader`` to your ``INSTALLED_APPS`` setting.
3. Add the uploader's urls::

   url(r'^upload/', include('uploader.urls')),

4. Write one or more upload handlers.
5. Go to /admin/uploader/upload/ to start uploading.


Writing an upload handler
=========================

.. note:: An upload handler does not have to exist within the application for which it creates records. It must simply be within an application that is imported so the handler can be discovered.

An upload handler assigns one or more MIME types to a function. There should only be one handler for a given MIME type, although Uploader does allow some overlap using '\*'. For example, you can have one handler that handles ``image/tiff`` and another that handles ``image/*`` and yet another that handles ``*/*``\ . The ``image/tiff`` handler would get any ``.tiff`` images, the ``image/*`` would get any other type of image and the ``*/*`` handler would get any other type of file.

To start, create a file named ``upload.py`` in your application. This file can contain several different handlers. When the Uploader application is first loaded, it attempts to import this file from every installed application.

A basic handler looks like this::

   from uploader.registration import upload_handlers

   def photo_handler(obj):
       """
       Handle the creation of a SimpleModel record from an uploaded image.
       """
       from .models import SimpleModel

       new_item = SimpleModel.objects.create(
           name=obj.filename,
           slug=obj.filename_slug,
           description='',
           file=obj.file_contents
       )

       return new_item
   photo_handler.thumbnail_attribute = 'thumb'

   upload_handlers.register(['image/jpeg', 'image/png'], photo_handler)

