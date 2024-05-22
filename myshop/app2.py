from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models import User, Product, CartItem, Order

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'CartItem': CartItem, 'Order': Order}

from views import main_views, auth_views, product_views, cart_views, order_views

app.register_blueprint(main_views.bp)
app.register_blueprint(auth_views.bp)
app.register_blueprint(product_views.bp)
app.register_blueprint(cart_views.bp)
app.register_blueprint(order_views.bp)

if __name__ == '__main__':
    app.run(debug=True)
