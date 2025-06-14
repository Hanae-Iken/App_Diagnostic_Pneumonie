from pymongo import MongoClient, ASCENDING
from config import MONGO_URI
from datetime import datetime
import bcrypt

def run_migration():
    try:
        client = MongoClient(MONGO_URI)
        db = client["mon_site"]
        
        print("🚀 Début de la migration...")
        
        # Test de connexion d'abord
        try:
            client.admin.command('ping')
            print("✅ Connexion MongoDB réussie")
        except Exception as e:
            print(f"❌ Erreur de connexion MongoDB: {e}")
            return False

        # --- USERS ---
        try:
            if 'users' not in db.list_collection_names():
                db.create_collection('users')
                print("✅ Collection 'users' créée.")
            
            # Essayer de créer l'index (peut échouer si pas assez d'espace)
            try:
                db.users.create_index([('email', ASCENDING)], unique=True)
                print("✅ Index unique sur email créé")
            except Exception as e:
                print(f"⚠️ Index email non créé: {e}")

            # Admin par défaut
            if db.users.count_documents({'email': 'admin@example.com'}) == 0:
                password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
                db.users.insert_one({
                    "username": "admin",
                    "email": "admin@example.com",
                    "password": password,
                    "role": "admin",
                    "created_at": datetime.utcnow()
                })
                print("👤 Admin ajouté dans 'users'.")
        except Exception as e:
            print(f"⚠️ Erreur collection users: {e}")

        # --- IMAGES MEDICALES ---
        try:
            if 'images' not in db.list_collection_names():
                db.create_collection('images')
                print("✅ Collection 'images' créée.")
            
            # Structure pour les images avec données patient
            try:
                db.images.create_index([('utilisateurId', ASCENDING)])
                db.images.create_index([('patient.cin', ASCENDING)])
                db.images.create_index([('dateUpload', ASCENDING)])
                print("✅ Index images créés")
            except Exception as e:
                print(f"⚠️ Index images non créés: {e}")
        except Exception as e:
            print(f"⚠️ Erreur collection images: {e}")

        # --- ANALYSES ---
        try:
            if 'analyses' not in db.list_collection_names():
                db.create_collection('analyses')
                print("✅ Collection 'analyses' créée.")
            
            try:
                db.analyses.create_index([('imageId', ASCENDING)])
                db.analyses.create_index([('utilisateurId', ASCENDING)])
                db.analyses.create_index([('dateAnalyse', ASCENDING)])
                print("✅ Index analyses créés")
            except Exception as e:
                print(f"⚠️ Index analyses non créés: {e}")
        except Exception as e:
            print(f"⚠️ Erreur collection analyses: {e}")

        print("🚀 Migration terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale de migration: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    if not success:
        print("\n💡 Solutions possibles:")
        print("1. Libérez de l'espace disque (recommandé)")
        print("2. Utilisez MongoDB Atlas (cloud)")
        print("3. Changez le répertoire de données MongoDB")