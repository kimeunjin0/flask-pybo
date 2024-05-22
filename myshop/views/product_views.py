from flask import Blueprint, render_template
from models import Product
from forms import EmptyForm

bp = Blueprint('product', __name__)

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = EmptyForm()
    return render_template('product_detail.html', product=product, form=form)
