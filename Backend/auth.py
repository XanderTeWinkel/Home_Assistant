from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timezone

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# --------------------------------------------------
# Authentication routes
# --------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Missing data"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "User already exists"}), 409

    user = User()
    user.username = data["username"]
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token})


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()  # this is a string UUID

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "created_at": user.created_at.astimezone(timezone.utc).isoformat()
    })



@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    data = request.json
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if not data or "old_password" not in data or "new_password" not in data:
        return jsonify({"message": "Missing data"}), 400

    if not user.check_password(data["old_password"]):
        return jsonify({"message": "Old password is incorrect"}), 400

    user.set_password(data["new_password"])
    db.session.commit()

    return jsonify({"message": "Password updated successfully"})
