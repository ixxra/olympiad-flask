__author__ = 'ixxra'
from PIL import Image


NORMAL_SIZE = (200, 200)
THUMBNAIL_SIZE = (50, 50)


def add(user, image, content_type):
    """
    Adds a User image and thumbnail to the database

    @param user: models.User instance
    @param image: image bytes or fp
    @param content_type: string describing images mime type
    """
    origin = Image.open(image)
    target = origin.resize(NORMAL_SIZE, Image.ANTIALIAS)
    thumb = origin.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    user.photo.put(target, content_type=content_type)
    user.thumbnail.put(thumb, content_type=content_type)

