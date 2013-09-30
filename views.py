from server import app
from models import Olympiad
from flask import render_template, request, url_for, redirect, abort, send_file
from flask.views import MethodView
from flask.ext.login import login_required, login_user, logout_user, current_user
import wiki
from flask import Markup
from auth import get_user


@app.route('/')
@app.route('/index')
def index():
    user = current_user
    try:
        title, html = wiki.content('International_Science_Olympiad')
    except:
        title, html = 'Olympic hub', 'Home page'

    if user.is_anonymous():
        return render_template('home.html', main_content=Markup(html))
    else:
        return render_template('home.html', user=user, main_content=Markup(html))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/me')
def me():
    user = current_user

    if user.is_anonymous():
        return redirect(url_for('login'))

    return render_template('me.html', user=user)


@app.route('/me/picture/upload', methods=['GET', 'POST'])
def picture():
    user = current_user

    if user.is_anonymous():
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('user_picture.html', user=user)
    else:
        file = request.files['image']
        user.photo.put(file, content_type=file.content_type)
        user.save()


@app.route('/me/picture')
def user_photo():
    user = current_user

    if user.is_anonymous():
        abort(404)

    return send_file(user.photo, mimetype=user.photo.content_type)


class Olympiads(MethodView):
    def get(self):
        user = current_user
        olympiads = Olympiad.objects.all()

        if user.is_anonymous():
            return render_template('olympiads.html', olympiads=olympiads)
        else:
            return render_template('olympiads.html', olympiads=olympiads, user=user)
    
    
class Login(MethodView):
    def get(self):
        return render_template('signin.html')

    def post(self):
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        if user is not None:
            remember = 'remember-me' in request.form
            if login_user(user, remember=remember):
                return redirect(url_for('index'))

        return render_template('signin.html')


app.add_url_rule('/olympiads/', view_func=Olympiads.as_view('olympiads'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
