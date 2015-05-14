# -*- coding: utf-8 -*-
from django.db import models


class SimpleModel(models.Model):
    """
    (SimpleModel description)
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file = models.ImageField(upload_to="pictures")
    thumb = models.ImageField(upload_to="picture_thumbs")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('simplemodel_detail_view_name', [str(self.id)])

    def make_thumbnail(self):
        if not self.file:
            return

        import mimetypes
        import os
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile

        # Set our max thumbnail size in a tuple (max width, max height)
        thumbnail_size = (99, 66)

        mtype = mimetypes.guess_type(self.file.name)[0]
        ext = os.path.splitext(self.file.name)[1]
        pil_type = mtype.split('/')[1]

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.file.read()))
        image.thumbnail(thumbnail_size, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, pil_type)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.file.name)[-1],
                temp_handle.read(), content_type=mtype)
        # Save SimpleUploadedFile into image field
        self.thumb.save(
            '%s_thumbnail%s' % (os.path.splitext(suf.name)[0], ext),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        if not self.id:
            self.make_thumbnail()
        super(SimpleModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(SimpleModel, self).delete(*args, **kwargs)
