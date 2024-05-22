from flask import Blueprint, render_template
from models import Product

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)
