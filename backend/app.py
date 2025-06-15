from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URI
from auth.routes import auth_bp
from afficher_les_resultats.results import results_bp
from db_migration import run_migration
from uploads.uploads import upload_bp
from afficher_les_resultats.historique import history_bp
from afficher_les_resultats.analyze import analyze_bp
from patients.routes import patients_bp  # ← Ajout de cette ligne

app = Flask(__name__)

# Configuration CORS simplifiée et plus permissive
CORS(app,
     origins=["http://localhost:3000", "http://localhost:3001"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

# Exécute la migration au démarrage
run_migration()

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client["mon_site"]

# Ajouter la base de données à l'app
app.config["db"] = db

# Enregistrer les routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(results_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(history_bp) 
app.register_blueprint(analyze_bp)
app.register_blueprint(patients_bp, url_prefix='/api')  # ← Cette ligne fonctionne maintenant

if __name__ == "__main__":
    app.run(debug=True)