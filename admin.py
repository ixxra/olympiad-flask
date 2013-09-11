from flask import request, redirect, url_for, render_template
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
#from flask_mongoengine.wtf import model_form
from server import app
from auth import requires_auth
from models import Product


@requires_auth
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/layout.djhtml')

@requires_auth
@app.route('/admin/stock')
def admin_stock():
    return render_template('admin/stock.djhtml')


class ManageStock(MethodView):
    decorators = [requires_auth]
    
    def get_context(self, obid=None):
        form_cls = model_form(Product, exclude=('created_at'))
        
        if obid is not None:
            product = Product.objects.get_or_404(id=obid)
            if request.method == 'POST':
                form = form_cls(request.form, initial=product._data, csrf_enabled=False)
            else:
                form = form_cls(obj=product, csrf_enabled=False)
        else:
            product = Product()
            form = form_cls(request.form, csrf_enabled=False)
            
        context = {
            'product' : product,
            'form' : form,
            'add' : obid is None
        }
        
        return context
    
    
    def get(self, obid):
        context = self.get_context(obid)
        return render_template('admin/detail.djhtml', **context)
    
    def post(self, obid):
        context = self.get_context(obid)
        form = context.get('form')
        
        if form.validate():
            product = context.get('product')
            form.populate_obj(product)
            product.save()

            return redirect(request.base_url)
        
        return render_template('admin/detail.djhtml', **context)

    
app.add_url_rule('/admin/stock/add/',
                 view_func=ManageStock.as_view('add'), 
                 defaults={'obid' : None})

app.add_url_rule('/admin/stock/edit/<obid>/', 
                 view_func=ManageStock.as_view('edit'))
