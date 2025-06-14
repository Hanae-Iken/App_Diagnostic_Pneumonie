from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from auth.utils import hash_password, check_password, generate_token, token_required, decode_token
from datetime import datetime

# CORRECTION: __name__ au lieu de **name**
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST", "OPTIONS"])  # Ajout OPTIONS
def signup():
    # Gestion des requêtes OPTIONS pour CORS
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        db = current_app.config["db"]
        data = request.get_json()
        
        # Validation des données
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
            
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not username or not email or not password:
            return jsonify({"error": "Tous les champs sont requis"}), 400
            
        # Vérification si l'email existe déjà
        if db.users.find_one({"email": email}):
            return jsonify({"error": "Email déjà utilisé"}), 400
            
        # Hash du mot de passe
        hashed = hash_password(password)
        
        # Création de l'utilisateur
        user = {
            "username": username,
            "email": email,
            "password": hashed,
            "role": "medecin",
            "profile": {},
            "created_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(user)
        
        return jsonify({
            "message": "Utilisateur créé avec succès",
            "user_id": str(result.inserted_id)
        }), 201
        
    except Exception as e:
        print(f"Erreur lors de l'inscription: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@auth_bp.route("/signin", methods=["POST"])
def signin():
    try:
        db = current_app.config["db"]
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
            
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Email et mot de passe requis"}), 400
            
        user = db.users.find_one({"email": email})
        
        if not user or not check_password(password, user["password"]):
            return jsonify({"error": "Email ou mot de passe incorrect"}), 401
            
        token = generate_token(user["_id"])
        
        return jsonify({
            "token": token,
            "username": user["username"],
            "role": user.get("role", "medecin")
        })
        
    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(user_id):
    try:
        db = current_app.config["db"]
        data = request.get_json()
        
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile": data}}
        )
        
        return jsonify({"message": "Profil mis à jour"})
        
    except Exception as e:
        print(f"Erreur lors de la mise à jour du profil: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    try:
        db = current_app.config["db"]
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
            
        email = data.get("email")
        
        if not email:
            return jsonify({"error": "Email requis"}), 400
            
        user = db.users.find_one({"email": email})
        
        if not user:
            return jsonify({"error": "Email introuvable"}), 404
            
        token = generate_token(user["_id"])
        
        return jsonify({
            "message": "Token de réinitialisation généré",
            "reset_token": token
        })
        
    except Exception as e:
        print(f"Erreur lors de la réinitialisation: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        db = current_app.config["db"]
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400
            
        token = data.get("token")
        new_password = data.get("new_password")
        
        if not token or not new_password:
            return jsonify({"error": "Token et nouveau mot de passe requis"}), 400
            
        user_id = decode_token(token)
        
        if not user_id:
            return jsonify({"error": "Token invalide ou expiré"}), 403
            
        hashed = hash_password(new_password)
        
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed}}
        )
        
        return jsonify({"message": "Mot de passe mis à jour avec succès"})
        
    except Exception as e:
        print(f"Erreur lors de la réinitialisation du mot de passe: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500
    