from datetime import datetime 
from server import db
from flask.ext.login import UserMixin


now = datetime.now


class User(db.Document, UserMixin):
    created_at = db.DateTimeField(default=now(), required=True)
    nickname = db.StringField(max_length=255, required=True)
    name = db.StringField(max_length=255, required=True)
    surname = db.StringField(max_length=255, required=True)
    dob = db.DateTimeField()
    #contests = [db.ReferenceField(Olympiad)]
    medals = None
    password_hash = db.StringField(max_length=255, required=True)
    google_login = None
    photo = db.ImageField(thumbnail_size=(32, 32, True))
    #thumbnail = db.FileField()

    def get(userid):
        try:
            u = User.objects.get(id=userid)
        except:
            u = None
        return u


class City(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    name = db.StringField(max_length=255, required=True)
    country = db.StringField(max_length=255, required=True)
    position = db.GeoPointField()


class Olympiad(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=now(), required=True)
    number = db.IntField(min_value=1)
    city = db.StringField(max_length=255, required=True)
    country = db.StringField(max_length=255, required=True)
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField(required=True)
    file = None
    logo = db.FileField()
    #category = db.ReferenceField(OlympiadCategory, required=True)
    #name = db.StringField(max_length=255, required=True)
    #contestants = [db.ReferenceField(User)]


class OlympiadCategory(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    name = db.StringField(max_length=255, required=True)
    abbreviation = db.StringField(max_length=10)
    url = db.URLField()
    events = db.ListField(db.EmbeddedDocumentField(Olympiad))
    logo = None


class Admin(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    user = db.ReferenceField(User)