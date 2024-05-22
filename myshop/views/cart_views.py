from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from models import CartItem, Product, db

bp = Blueprint('cart', __name__)

@bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = CartItem(product_id=product_id, user_id=current_user.id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

@bp.route('/cart/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    data = request.get_json()
    quantity = data.get('quantity')
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)
