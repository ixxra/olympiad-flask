from server import login_manager
from models import User
from werkzeug import check_password_hash


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


def get_user(username, password):
    try:
        user = User.objects.get(nickname=username)
        if not check_password_hash(user.password_hash, password):
            user = None
    except:
        user = None

    return user