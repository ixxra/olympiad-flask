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
    photo = db.FileField()

    def get(userid):
        try:
            u = User.objects.get(id=userid)
        except:
            u = None
        return u


class OlympiadCategory(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    name = db.StringField(max_length=255, required=True)
    logo = None


class City(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    name = db.StringField(max_length=255, required=True)
    country = db.StringField(max_length=255, required=True)
    lat = db.NumericField()
    long = db.NumericField()


class Olympiad(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    category = db.ReferenceField(OlympiadCategory, required=True)
    name = db.StringField(max_length=255, required=True)
    city = db.ReferenceField(City)
    logo = db.FileField()
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField(required=True)
    file = None
    cotestants = [db.ReferenceField(User)]


class Admin(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    user = db.ReferenceField(User)