from flask import Blueprint, jsonify, request
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.models import User, db

auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    if "@" not in email:
        return jsonify({
            "message": "A valid email is required"
        }), 400

    if len(password) < 6:
        return jsonify({
            "message": "Password must contain at least 6 characters"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "A user with this email already exists"
        }), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    login_user(user)

    return jsonify({
        "message": "Logged in",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 200


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    return jsonify({
        "message": "Logged out"
    }), 200


@auth.route("/me", methods=["GET"])
def current_user_details():
    if not current_user.is_authenticated:
        return jsonify({
            "authenticated": False
        }), 200

    return jsonify({
        "authenticated": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "is_admin": current_user.is_admin
        }
    }), 200
