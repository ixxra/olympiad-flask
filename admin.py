from flask import request, redirect, url_for, render_template, abort
#from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from server import app
from flask.ext.login import login_required
from auth import permission_required
from models import OlympiadCategory, Olympiad
from wtforms.ext.dateutil.fields import DateField


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


@permission_required
@login_required
@app.route('/admin/categories/<oid>')
def show_category(oid):
    category = OlympiadCategory.objects.get_or_404(id=oid)
    return render_template('admin/category_groups.html', category=category)


@permission_required
@login_required
@app.route('/admin/categories/<oid>/add', methods=('GET', 'POSt'))
def create_event(oid):
    OlympiadForm = model_form(Olympiad)
    OlympiadForm.start_date = DateField()
    OlympiadForm.end_date = DateField()
    form = OlympiadForm(request.form, csrf_enabled=False)
    form.start_date.widget.input_type = 'date'
    form.end_date.widget.input_type = 'date'
    
    if form.validate_on_submit():
        category = OlympiadCategory.objects.get_or_404(id=oid)
        new_event = Olympiad()
        form.populate_obj(new_event)
        category.events.append(new_event)
        category.save()
        url = request.form['callback_url']
        return redirect(url)
    
    category = OlympiadCategory.objects.get_or_404(id=oid)
    return render_template('admin/olympiad_new.html', category=category, form=form)



