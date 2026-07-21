from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.models import Product, db


products = Blueprint(
    "products",
    __name__,
    url_prefix="/api"
)


@products.route("/products", methods=["GET"])
def get_products():
    all_products = Product.query.order_by(
        Product.created_at.desc()
    ).all()

    return jsonify([
        product.to_dict()
        for product in all_products
    ]), 200


@products.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict()), 200


@products.route("/products", methods=["POST"])
@login_required
def create_product():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    description = str(data.get("description", "")).strip()
    image_url = data.get("image_url")

    if not name:
        return jsonify({
            "message": "Product name is required"
        }), 400

    if data.get("price") is None:
        return jsonify({
            "message": "Product price is required"
        }), 400

    try:
        price = float(data["price"])
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return jsonify({
            "message": "Price must be a number and stock must be an integer"
        }), 400

    if price < 0:
        return jsonify({
            "message": "Price cannot be negative"
        }), 400

    if stock < 0:
        return jsonify({
            "message": "Stock cannot be negative"
        }), 400

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created",
        "product": product.to_dict()
    }), 201


@products.route(
    "/products/<int:product_id>",
    methods=["PUT"]
)
@login_required
def update_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    data = request.get_json(silent=True) or {}

    if "name" in data:
        name = str(data["name"]).strip()

        if not name:
            return jsonify({
                "message": "Product name cannot be empty"
            }), 400

        product.name = name

    if "description" in data:
        product.description = str(
            data["description"]
        ).strip()

    if "price" in data:
        try:
            price = float(data["price"])
        except (TypeError, ValueError):
            return jsonify({
                "message": "Price must be a number"
            }), 400

        if price < 0:
            return jsonify({
                "message": "Price cannot be negative"
            }), 400

        product.price = price

    if "stock" in data:
        try:
            stock = int(data["stock"])
        except (TypeError, ValueError):
            return jsonify({
                "message": "Stock must be an integer"
            }), 400

        if stock < 0:
            return jsonify({
                "message": "Stock cannot be negative"
            }), 400

        product.stock = stock

    if "image_url" in data:
        product.image_url = data["image_url"]

    db.session.commit()

    return jsonify({
        "message": "Product updated",
        "product": product.to_dict()
    }), 200


@products.route(
    "/products/<int:product_id>",
    methods=["DELETE"]
)
@login_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted"
    }), 200
