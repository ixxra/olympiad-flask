from server import login_manager
from models import User, Admin
from werkzeug import check_password_hash
from flask.ext.login import current_user


class UserCantAdminError(Exception):
    pass

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


def permission_required(f):
    def new_func(*args, **kwargs):
        u = current_user
        if u.is_anonymous():
            print('no one is logged in!!')
        else:
            print ('user logged in!!')

        try:
            admin = Admin.objects.get(user=u)
            print ('no exception')
        except:
            print ('exception')
            raise UserCantAdminError('Not a valid admin')

        return f(*args, **kwargs)

    return new_func