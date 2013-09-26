from server import login_manager
from models import User


@login_manager.user_loader
def get_user(userid):
    return User.get(userid)
