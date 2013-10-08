from views import *
from admin import *
from server import app
from werkzeug import run_simple
import config

#app.run()

run_simple('localhost', 5000, app, use_debugger=True, use_reloader=True, use_evalex=True)
