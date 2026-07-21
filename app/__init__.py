from flask import Flask, jsonify, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import Product, User, db
from config import Config


login_manager = LoginManager()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "message": "Authentication required"
    }), 401


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth
    from app.routes.products import products
    from app.routes.cart import cart
    from app.routes.orders import orders

    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    app.register_blueprint(orders)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Ecommerce API is running",
            "endpoints": {
                "register": "POST /auth/register",
                "login": "POST /auth/login",
                "logout": "POST /auth/logout",
                "products_api": "GET /api/products",
                "product_catalog": "GET /products",
                "shopping_cart": "GET /cart"
            }
        }), 200

    @app.route("/products", methods=["GET"])
    def product_catalog():
        all_products = Product.query.order_by(
            Product.created_at.desc()
        ).all()

        return render_template(
            "products.html",
            products=all_products
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "message": "Resource not found"
        }), 404

    return app
