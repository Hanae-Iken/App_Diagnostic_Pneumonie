import bcrypt
import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET
from flask import request, jsonify

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Middleware pour route protégée
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({'error': 'Token manquant'}), 401

        # ➕ Ici on enlève le préfixe "Bearer " si présent
        if token.startswith("Bearer "):
            token = token[7:]

        user_id = decode_token(token)
        if not user_id:
            return jsonify({'error': 'Token invalide'}), 403

        return f(user_id, *args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator

