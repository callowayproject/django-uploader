# encoding: utf-8
import mimetypes

from django.db import models
from settings import STORAGE_CLASS
from django.core.files.storage import get_storage_class
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


UploadStorageClass = get_storage_class(STORAGE_CLASS)


class Upload(models.Model):
    """
    An uploaded file.
    """
    uploaded_file = models.FileField(
        upload_to="uploads",
        storage=UploadStorageClass())
    date_uploaded = models.DateTimeField(auto_now_add=True)
    admin_url = models.CharField(
        blank=True,
        max_length=255,
        default="")
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    thumbnail_attr = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        default="")

    def __unicode__(self):
        return self.filename

    @property
    def filename(self):
        import os
        return os.path.basename(self.uploaded_file.name.encode('utf8')).decode('utf8')

    @property
    def filename_slug(self):
        from django.utils.text import slugify
        return slugify(self.filename)

    @property
    def file_contents(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        return SimpleUploadedFile(self.filename,
            self.uploaded_file.read(),
            content_type=self.mimetype)

    @property
    def mimetype(self):
        return mimetypes.guess_type(self.filename)[0]

    def save(self, *args, **kwargs):
        self.slug = self.uploaded_file.name
        super(Upload, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.uploaded_file.delete(False)
        super(Upload, self).delete(*args, **kwargs)
