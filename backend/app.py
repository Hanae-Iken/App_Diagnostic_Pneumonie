from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URI
from auth.routes import auth_bp

app = Flask(__name__)
CORS(app)

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client["mon_site"]

# Ajouter la base de données à l'app


app.config["db"] = db

# Enregistrer les routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(debug=True)
