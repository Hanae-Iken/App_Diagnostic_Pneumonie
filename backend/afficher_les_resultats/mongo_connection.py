from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Charger les variables d’environnement depuis .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "mon_site")  # ou remplace par "fmpt_db"

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ✅ Collections exportables
analyses_collection = db["analyses"]
users_collection = db["users"]
images_collection = db["images"]

# ✅ Fonction d’accès à la base
def get_db():
    return db
