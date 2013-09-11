from server import app
from models import User, Olympiad
from flask import render_template, request, url_for, flash, redirect
from flask.views import MethodView
from flask.ext.login import login_required, login_user, logout_user, current_user
from auth import get_user


@app.route('/')
@app.route('/index')
def index():
    user = current_user
    if user.is_anonymous():
        return render_template('layout.djhtml')
    else:
        return render_template('layout.djhtml', user=user)


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


class Stock(MethodView):
    def get(self):
        user = current_user
        products = Product.objects.all()

        if user.is_anonymous():
            return render_template('stock.djhtml', products=products)
        else:
            return render_template('stock.djhtml', products=products, user=user)
    
    
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
        

app.add_url_rule('/stock/', view_func=Stock.as_view('stock'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
