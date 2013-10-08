__author__ = 'ixxra'
from PIL import Image
from io import BytesIO

NORMAL_SIZE = (200, 200)
THUMBNAIL_SIZE = (50, 50)


def add(user, image, content_type):
    """
    Adds a User image and thumbnail to the database

    @param user: models.User instance
    @param image: image bytes or fp
    @param content_type: string describing images mime type
    """
    #file_content = TemporaryFile()
    #image.save(file_content)
    #file_content.seek(0)
    print ('image:', type(image), image.tell())
    origin = Image.open(image)
    print ('opened', origin.format)
    target = origin.resize(NORMAL_SIZE, Image.ANTIALIAS)
    print ('target', target, target.format)
    origin.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    target_data = BytesIO()
    print ('bytes')
    thumb_data = BytesIO()
    print ('bytes')
    print (target.format)
    target.save(target_data, format='JPEG')
    print ('save')
    origin.save(thumb_data, format='JPEG')
    print ('save')
    target_data.seek(0)
    print ('seek')
    thumb_data.seek(0)
    print ('seek')
    print (user, user.thumbnail, user.photo, user.nickname)
    #user.photo.put(target_data, content_type='image/jpeg')
    #print ('user_photo')
    user.thumbnail.put(thumb_data, content_type='image/jpeg')
    print ('user_thumb')
    user.save()
    print ('save')
