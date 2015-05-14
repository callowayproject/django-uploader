
******
Models
******

.. py:module:: uploader.models

.. py:class:: Upload

   An uploaded file.

   .. py:attribute:: uploaded_file

      :py:class:`FileField` containing the uploaded file.

   .. py:attribute:: date_uploaded

      :py:class:`DateTimeField` auto populated with the date and time the file was uploaded.

   .. py:attribute:: admin_url

      :py:class:`CharField`\ (255) stores the admin url of the object the upload handler returns.

   .. py:attribute:: content_type

      :py:class:`ForeignKey`\ (:py:class:`ContentType`\ ) stores the content type of the object the upload handler returns.

   .. py:attribute:: object_id

      :py:class:`PositiveIntegerField` stores the id of the object the upload handler returns.

   .. py:attribute:: related_object

      :py:class:`GenericForeignKey` is a generic link to the object the upload handler returns.

   .. py:attribute:: thumbnail_attr

      :py:class:`CharField`\ (255) stores the attribute of the ``related_object`` from which it can get a thumbnail.

   .. py:attribute:: filename

      *Read Only* Returns the filename of :py:attr:`uploaded_file`\ .

   .. py:attribute:: filename_slug

      *Read Only* Returns the filename of :py:attr:`uploaded_file` after applying the ``slugify`` filter.

   .. py:attribute:: file_contents

      *Read Only* Returns the contents of :py:attr:`uploaded_file` wrapped as a :py:class:`SimpleUploadedFile` that is assignable directly to a :py:class:`FileField` or :py:class:`ImageField`\ .

   .. py:attribute:: mimetype

      *Read Only* Returns the mimetype of :py:attr:`uploaded_file`\ .
