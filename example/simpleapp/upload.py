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
