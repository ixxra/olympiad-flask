from flask import request, redirect, url_for, render_template, abort
#from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from server import app
from flask.ext.login import login_required
from auth import permission_required
from models import OlympiadCategory
import flask.ext.mongoengine.wtf


#@requires_auth
#@app.route('/admin', methods=['GET', 'POST'])
#def admin():
#    return render_template('admin/layout.djhtml')


@permission_required
@login_required
@app.route('/admin/categories', methods=('GET', 'POST'))
def admin_categories():
    action = request.args.get('action', '')
    oid = request.args.get('id', '')

    if action == 'remove':
        sentenced = OlympiadCategory.objects.get(id=oid)
        sentenced.delete()
        sentenced.save()

    elif action == 'edit':
        edited = OlympiadCategory.objects.get(id=oid)
        print (edited.id)
        print (edited.url)
        OlympiadCategoryForm = model_form(OlympiadCategory)
        form = OlympiadCategoryForm(request.form, obj=edited, csrf_enabled=False)
        if form.validate_on_submit():
            form.populate_obj(edited)
            edited.save()
            print (edited.id)
            print (edited.url)
            url = request.form['callback_url']
            return redirect(url)
        return render_template('admin/categories_edit.html', form=form, oid=oid)

    return render_template('admin/categories.html', categories=OlympiadCategory.objects)


@permission_required
@login_required
@app.route('/admin/categories/edit')
def admin_categories_edit():
    return 'Categories editor'


@permission_required
@login_required
@app.route('/admin/categories/new', methods=('GET', 'POST'))
def create_category():
    OlympiadCategoryForm = model_form(OlympiadCategory)
    form = OlympiadCategoryForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        form.save()
        url = request.form['callback_url']
        #url_for('categories')
        return redirect(url)
    return render_template('admin/categories_new.html', form=form)