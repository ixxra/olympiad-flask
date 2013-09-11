from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app= Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB' : 'olympiad'}
app.config['SECRET_KEY'] = '123456'
db=MongoEngine(app)
login_manager= LoginManager()
login_manager.init_app(app)
