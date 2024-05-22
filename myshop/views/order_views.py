from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Order, CartItem, db
from datetime import datetime

bp = Blueprint('order', __name__)


@bp.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order_history.html', orders=orders)


@bp.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Here you can create an order and clear the cart
    new_order = Order(user_id=current_user.id, total_amount=total_amount)
    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return render_template('checkout.html', total_amount=total_amount)
