from flask import Blueprint, jsonify, redirect, render_template, session, url_for
from flask_login import current_user

from app.models import Order, Product, User, db


orders = Blueprint("orders", __name__)


def get_order_user():
    """
    Use the logged-in user when available.
    Otherwise, use the first existing user for this course demo.
    """
    if current_user.is_authenticated:
        return current_user

    return User.query.first()


@orders.route("/orders", methods=["GET"])
def order_history():
    user = get_order_user()

    if user is None:
        return render_template(
            "orders.html",
            orders=[]
        )

    user_orders = Order.query.filter_by(
        user_id=user.id
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders
    )


@orders.route("/orders/place", methods=["POST"])
def place_order():
    user = get_order_user()

    if user is None:
        return jsonify({
            "message": "Create or register a user before placing an order"
        }), 400

    cart_ids = session.get("cart", [])

    if not cart_ids:
        return redirect(url_for("cart.view_cart"))

    total = 0

    for product_id in cart_ids:
        product = db.session.get(Product, product_id)

        if product:
            total += product.price

    if total <= 0:
        return redirect(url_for("cart.view_cart"))

    order = Order(
        user_id=user.id,
        total=total,
        status="Placed"
    )

    db.session.add(order)
    db.session.commit()

    session["cart"] = []

    return redirect(url_for("orders.order_history"))
