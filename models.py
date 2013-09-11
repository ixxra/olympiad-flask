from datetime import datetime 
from server import db
from flask.ext.login import UserMixin


now = datetime.now


class User(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    name = db.StringField(max_length=255, required=True)
    surname = db.StringField(max_length=255, required=True)
    dob = db.DateTimeField()
    #contests = [db.ReferenceField(Olympiad)]
    medals = None
    password_hash = db.StringField(max_length=255, required=True)
    google_login = None


class Olympiad(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    category = db.StringField(max_length=255, required=True)
    name = db.StringField(max_length=255, required=True)
    city = None
    logo = None
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField(required=True)
    file = None
    cotestants = [db.ReferenceField(User)]


class Admin(db.Document):
    created_at = db.DateTimeField(default=now(), required=True)
    user = db.ReferenceField(User)        