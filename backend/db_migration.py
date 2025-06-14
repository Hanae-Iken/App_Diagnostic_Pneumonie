from afficher_les_resultats.mongo_connection import get_db
from pymongo import ASCENDING
import bcrypt
from datetime import datetime

def run_migration():
    db = get_db()

    # --- USERS ---
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
        db.users.create_index([('email', ASCENDING)], unique=True)
        print("✅ Collection 'users' créée.")

    # Admin par défaut
    if db.users.count_documents({'email': 'admin@admin.com'}) == 0:
        password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        db.users.insert_one({
            "nom": "admin",
            "email": "admin@admin.com",
            "motDePasse": password,
            "role": "administrateur"
        })
        print("👤 Admin ajouté dans 'users'.")

    # --- IMAGES MEDICALES ---
    if 'images' not in db.list_collection_names():
        db.create_collection('images')
        db.images.create_index([('utilisateurId', ASCENDING)])
        print("📂 Collection 'images' créée.")

    # --- ANALYSES ---
    if 'analyses' not in db.list_collection_names():
        db.create_collection('analyses')
        db.analyses.create_index([('imageId', ASCENDING)])
        db.analyses.create_index([('utilisateurId', ASCENDING)])
        print("📊 Collection 'analyses' créée.")

    print("🚀 Migration terminée.")

if __name__ == "__main__":
    run_migration()