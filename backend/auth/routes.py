from flask import Blueprint, request, jsonify,current_app
from bson.objectid import ObjectId
from auth.utils import hash_password, check_password, generate_token, token_required
from datetime import datetime


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    db = current_app.config["db"]
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if db.users.find_one({"email": email}):
        return jsonify({"error": "Email déjà utilisé"}), 400

    hashed = hash_password(password)

    user = {
        "username": username,
        "email": email,
        "password": hashed,
        "profile": {},
        "created_at": datetime.utcnow()
    }
    db.users.insert_one(user)
    return jsonify({"message": "Utilisateur créé"}), 201


@auth_bp.route("/signin", methods=["POST"])
def signin():
    db = current_app.config["db"]
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = db.users.find_one({"email": email})
    if not user or not check_password(password, user["password"]):
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

    token = generate_token(user["_id"])
    return jsonify({"token": token, "username": user["username"]})


@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(user_id):
    db = current_app.config["db"]
    data = request.get_json()

    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"profile": data}}
    )
    return jsonify({"message": "Profil mis à jour"})
