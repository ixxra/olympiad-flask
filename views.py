from server import app
from models import User, Olympiad
from flask import render_template, request, url_for, flash, redirect
from flask.views import MethodView
from flask.ext.login import login_required, login_user, logout_user, current_user
import wiki
from flask import Markup
#from auth import get_user


@app.route('/')
@app.route('/index')
def index():
    user = current_user
    title, html = wiki.content('International_Science_Olympiad')

    if user.is_anonymous():
        return render_template('home.html', main_content=Markup(html))
    else:
        return render_template('home.html', user=user, main_content=Markup(html))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/cashier')
@login_required
def cashier():
    user = current_user

    if user.is_anonymous():
        return render_template('cashier.djhtml')

    return render_template('cashier.djhtml', user=user)


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
        user = get_user(request.form['username'], request.form['password'])
        
        if user is not None:
            remember = 'remember-me' in request.form
            if login_user(user, remember=remember):
                flash('logged in successfully')
                return redirect(request.form['redirect_url'] or url_for('index'))

        return render_template('signin.html')
        

app.add_url_rule('/olympiads/', view_func=Olympiads.as_view('olympiads'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
