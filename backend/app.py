from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URI
from auth.routes import auth_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from afficher_les_resultats.results import results_bp
app = Flask(__name__)
CORS(app)

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client["mon_site"]

# Ajouter la base de données à l'app


app.config["db"] = db

# Enregistrer les routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(results_bp)

if __name__ == "__main__":
    app.run(debug=True)

