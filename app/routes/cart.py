from flask import Blueprint, redirect, render_template, session, url_for

from app.models import Product


cart = Blueprint("cart", __name__)


@cart.route("/cart")
def view_cart():
    cart_ids = session.get("cart", [])

    products = []
    total = 0

    for product_id in cart_ids:
        product = Product.query.get(product_id)

        if product:
            products.append(product)
            total += product.price

    return render_template(
        "cart.html",
        products=products,
        total=total
    )


@cart.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    cart_ids = session.get("cart", [])
    cart_ids.append(product.id)
    session["cart"] = cart_ids

    return redirect(url_for("product_catalog"))


@cart.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_ids = session.get("cart", [])

    if product_id in cart_ids:
        cart_ids.remove(product_id)

    session["cart"] = cart_ids

    return redirect(url_for("cart.view_cart"))
