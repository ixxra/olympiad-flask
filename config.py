__author__ = 'ixxra'
from server import login_manager

login_manager.login_view = 'login'

user_roles = ('admin', 'user')
user_actions = ('create', 'delete', 'edit')