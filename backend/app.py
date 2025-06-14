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


app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    app.run(debug=True)

