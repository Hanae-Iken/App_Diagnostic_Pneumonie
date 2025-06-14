from pymongo import MongoClient, ASCENDING, DESCENDING
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
                    "created_at": datetime.utcnow(),
                    "last_login": None,
                    "is_active": True
                })
                print("👤 Admin ajouté dans 'users'.")
                
        except Exception as e:
            print(f"⚠️ Erreur collection users: {e}")
            
        # --- IMAGES MEDICALES (MISE À JOUR) ---
        try:
            if 'images' not in db.list_collection_names():
                db.create_collection('images')
                print("✅ Collection 'images' créée.")
           
            # Index pour les images avec nouvelles fonctionnalités
            try:
                db.images.create_index([('utilisateurId', ASCENDING)])
                db.images.create_index([('patient.cin', ASCENDING)])
                db.images.create_index([('dateUpload', DESCENDING)])  # DESC pour tri récent
                db.images.create_index([('statut', ASCENDING)])  # Nouveau
                db.images.create_index([('pret_pour_analyse', ASCENDING)])  # Nouveau
                db.images.create_index([('type_examen', ASCENDING)])  # Nouveau
                db.images.create_index([('analyseId', ASCENDING)])  # Nouveau - pour lien avec analyses
                print("✅ Index images créés avec nouvelles fonctionnalités")
            except Exception as e:
                print(f"⚠️ Index images non créés: {e}")
                
            # Mise à jour des documents existants pour compatibilité
            try:
                # Ajouter les nouveaux champs aux documents existants
                result = db.images.update_many(
                    {'statut': {'$exists': False}},  # Documents sans le champ statut
                    {
                        '$set': {
                            'statut': 'upload_complete',
                            'pret_pour_analyse': True,
                            'type_examen': 'radiographie',
                            'version_schema': '2.0',
                            'dateModification': datetime.utcnow()
                        }
                    }
                )
                if result.modified_count > 0:
                    print(f"✅ {result.modified_count} images mises à jour avec nouveaux champs")
                    
                # Valider la structure des patients
                result = db.images.update_many(
                    {'patient.dateNaissance': {'$exists': False}},
                    {
                        '$set': {
                            'patient.dateNaissance': None,
                            'patient.telephone': '',
                            'patient.adresse': '',
                            'patient.antecedents': []
                        }
                    }
                )
                if result.modified_count > 0:
                    print(f"✅ {result.modified_count} profils patients enrichis")
                    
            except Exception as e:
                print(f"⚠️ Erreur mise à jour images existantes: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur collection images: {e}")
            
        # --- NOUVELLE COLLECTION ANALYSES ---
        try:
            if 'analyses' not in db.list_collection_names():
                db.create_collection('analyses')
                print("✅ Collection 'analyses' créée.")
                
            # Index pour les analyses
            try:
                db.analyses.create_index([('imageId', ASCENDING)])
                db.analyses.create_index([('utilisateurId', ASCENDING)])
                db.analyses.create_index([('dateAnalyse', DESCENDING)])
                db.analyses.create_index([('patient.cin', ASCENDING)])
                db.analyses.create_index([('resultats.resultat', ASCENDING)])
                db.analyses.create_index([('statut', ASCENDING)])
                # Index composé pour recherches complexes
                db.analyses.create_index([
                    ('utilisateurId', ASCENDING), 
                    ('dateAnalyse', DESCENDING)
                ])
                print("✅ Index analyses créés")
            except Exception as e:
                print(f"⚠️ Index analyses non créés: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur collection analyses: {e}")
            
        # --- NOUVELLE COLLECTION RAPPORTS ---
        try:
            if 'rapports' not in db.list_collection_names():
                db.create_collection('rapports')
                print("✅ Collection 'rapports' créée.")
                
            # Index pour les rapports
            try:
                db.rapports.create_index([('analyseId', ASCENDING)])
                db.rapports.create_index([('utilisateurId', ASCENDING)])
                db.rapports.create_index([('dateGeneration', DESCENDING)])
                db.rapports.create_index([('type_rapport', ASCENDING)])
                print("✅ Index rapports créés")
            except Exception as e:
                print(f"⚠️ Index rapports non créés: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur collection rapports: {e}")
            
        # --- COLLECTION LOGS SYSTÈME ---
        try:
            if 'logs_systeme' not in db.list_collection_names():
                db.create_collection('logs_systeme')
                print("✅ Collection 'logs_systeme' créée.")
                
            # Index TTL pour auto-suppression après 30 jours
            try:
                db.logs_systeme.create_index([('timestamp', ASCENDING)], expireAfterSeconds=2592000)  # 30 jours
                db.logs_systeme.create_index([('niveau', ASCENDING)])
                db.logs_systeme.create_index([('utilisateurId', ASCENDING)])
                db.logs_systeme.create_index([('action', ASCENDING)])
                print("✅ Index logs_systeme créés avec TTL")
            except Exception as e:
                print(f"⚠️ Index logs_systeme non créés: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur collection logs_systeme: {e}")
            
        # --- COLLECTION STATISTIQUES ---
        try:
            if 'statistiques' not in db.list_collection_names():
                db.create_collection('statistiques')
                print("✅ Collection 'statistiques' créée.")
                
            # Index pour les statistiques 
            try:
                db.statistiques.create_index([('type', ASCENDING)])
                db.statistiques.create_index([('periode', ASCENDING)])
                db.statistiques.create_index([('utilisateurId', ASCENDING)])
                db.statistiques.create_index([('dateCalcul', DESCENDING)])
                print("✅ Index statistiques créés")
            except Exception as e:
                print(f"⚠️ Index statistiques non créés: {e}")
                
            # Initialiser les statistiques de base
            try:
                if db.statistiques.count_documents({'type': 'global'}) == 0:
                    db.statistiques.insert_one({
                        'type': 'global',
                        'periode': 'total',
                        'donnees': {
                            'total_analyses': 0,
                            'total_utilisateurs': db.users.count_documents({}),
                            'total_images': db.images.count_documents({}),
                            'analyses_normales': 0,
                            'analyses_pneumonie': 0,
                            'precision_moyenne': 0.0
                        },
                        'dateCalcul': datetime.utcnow(),
                        'version': '1.0'
                    })
                    print("✅ Statistiques globales initialisées")
            except Exception as e:
                print(f"⚠️ Erreur initialisation statistiques: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur collection statistiques: {e}")
            
        # --- COLLECTION CONFIGURATIONS ---
        try:
            if 'configurations' not in db.list_collection_names():
                db.create_collection('configurations')
                print("✅ Collection 'configurations' créée.")
                
            # Index pour les configurations
            try:
                db.configurations.create_index([('cle', ASCENDING)], unique=True)
                db.configurations.create_index([('categorie', ASCENDING)])
                print("✅ Index configurations créés")
            except Exception as e:
                print(f"⚠️ Index configurations non créés: {e}")
                
            # Configurations par défaut
            try:
                configurations_defaut = [
                    {
                        'cle': 'seuil_confiance_analyse',
                        'valeur': 0.7,
                        'description': 'Seuil de confiance minimum pour l\'analyse IA',
                        'categorie': 'ia',
                        'type': 'float',
                        'dateModification': datetime.utcnow()
                    },
                    {
                        'cle': 'taille_max_fichier_mb',
                        'valeur': 10,
                        'description': 'Taille maximale des fichiers en MB',
                        'categorie': 'upload',
                        'type': 'int',
                        'dateModification': datetime.utcnow()
                    },
                    {
                        'cle': 'formats_autorises',
                        'valeur': ['.png', '.jpg', '.jpeg', '.dcm'],
                        'description': 'Formats de fichiers autorisés',
                        'categorie': 'upload',
                        'type': 'list',
                        'dateModification': datetime.utcnow()
                    },
                    {
                        'cle': 'retention_logs_jours',
                        'valeur': 30,
                        'description': 'Durée de rétention des logs en jours',
                        'categorie': 'systeme',
                        'type': 'int',
                        'dateModification': datetime.utcnow()
                    },
                    {
                        'cle': 'email_notifications_actives',
                        'valeur': True,
                        'description': 'Activation des notifications par email',
                        'categorie': 'notifications',
                        'type': 'bool',
                        'dateModification': datetime.utcnow()
                    }
                ]
                
                for config in configurations_defaut:
                    if db.configurations.count_documents({'cle': config['cle']}) == 0:
                        db.configurations.insert_one(config)
                        
                print("✅ Configurations par défaut ajoutées")
            except Exception as e:
                print(f"⚠️ Erreur ajout configurations: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur collection configurations: {e}")
            
        # --- VÉRIFICATIONS FINALES ET NETTOYAGE ---
        try:
            print("\n🔍 Vérifications finales...")
            
            # Vérifier les collections
            collections = db.list_collection_names()
            collections_attendues = ['users', 'images', 'analyses', 'rapports', 'logs_systeme', 'statistiques', 'configurations']
            
            for col in collections_attendues:
                if col in collections:
                    count = db[col].count_documents({})
                    print(f"✅ {col}: {count} documents")
                else:
                    print(f"❌ {col}: collection manquante")
                    
            # Statistiques de migration
            total_users = db.users.count_documents({})
            total_images = db.images.count_documents({})
            total_analyses = db.analyses.count_documents({})
            
            print(f"\n📊 Résumé de la migration:")
            print(f"👥 Utilisateurs: {total_users}")
            print(f"🖼️ Images: {total_images}")
            print(f"🔬 Analyses: {total_analyses}")
            
            # Log de la migration
            try:
                db.logs_systeme.insert_one({
                    'action': 'migration_complete',
                    'niveau': 'INFO',
                    'message': f'Migration terminée - {total_users} users, {total_images} images, {total_analyses} analyses',
                    'timestamp': datetime.utcnow(),
                    'utilisateurId': None,
                    'metadata': {
                        'version_migration': '2.0',
                        'collections_creees': len(collections_attendues),
                        'duree_migration': 'calcul_requis'
                    }
                })
            except Exception as e:
                print(f"⚠️ Erreur log migration: {e}")
                
        except Exception as e:
            print(f"⚠️ Erreur vérifications finales: {e}")
            
        print("\n🎉 Migration terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale de migration: {e}")
        return False
        
    finally:
        try:
            client.close()
            print("🔌 Connexion MongoDB fermée")
        except:
            pass


def verification_post_migration():
    """
    Vérifie l'intégrité après migration
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client["mon_site"]
        
        print("\n🔍 Vérification post-migration...")
        
        # Vérifier les index
        collections_a_verifier = {
            'users': ['email_1'],
            'images': ['utilisateurId_1', 'patient.cin_1', 'statut_1'],
            'analyses': ['imageId_1', 'utilisateurId_1', 'dateAnalyse_-1'],
            'logs_systeme': ['timestamp_1'],
            'configurations': ['cle_1']
        }
        
        for collection, index_attendus in collections_a_verifier.items():
            if collection in db.list_collection_names():
                index_info = db[collection].list_indexes()
                index_noms = [idx['name'] for idx in index_info]
                
                for idx_attendu in index_attendus:
                    if idx_attendu in index_noms:
                        print(f"✅ {collection}.{idx_attendu}")
                    else:
                        print(f"⚠️ {collection}.{idx_attendu} manquant")
                        
        # Vérifier la cohérence des données
        images_avec_analyses = db.images.count_documents({'analyseId': {'$exists': True}})
        analyses_total = db.analyses.count_documents({})
        
        print(f"\n📊 Cohérence des données:")
        print(f"Images avec analyses: {images_avec_analyses}")
        print(f"Total analyses: {analyses_total}")
        
        if images_avec_analyses <= analyses_total:
            print("✅ Cohérence données OK")
        else:
            print("⚠️ Incohérence détectée")
            
        print("✅ Vérification post-migration terminée")
        
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
    finally:
        try:
            client.close()
        except:
            pass


def rollback_migration():
    """
    Fonction de rollback en cas de problème
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client["mon_site"]
        
        print("⚠️ ROLLBACK EN COURS...")
        
        # Sauvegarder les nouvelles collections avant suppression
        nouvelles_collections = ['analyses', 'rapports', 'logs_systeme', 'statistiques', 'configurations']
        
        for collection in nouvelles_collections:
            if collection in db.list_collection_names():
                # Créer une sauvegarde
                backup_name = f"{collection}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                db[collection].aggregate([{'$out': backup_name}])
                print(f"💾 Sauvegarde: {collection} -> {backup_name}")
                
                # Supprimer la collection
                db[collection].drop()
                print(f"🗑️ Collection {collection} supprimée")
                
        # Restaurer les anciens champs des images
        result = db.images.update_many(
            {'version_schema': '2.0'},
            {
                '$unset': {
                    'statut': '',
                    'pret_pour_analyse': '',
                    'type_examen': '',
                    'version_schema': '',
                    'analyseId': '',
                    'dateModification': ''
                }
            }
        )
        
        print(f"↩️ {result.modified_count} images restaurées")
        print("✅ Rollback terminé")
        
    except Exception as e:
        print(f"❌ Erreur rollback: {e}")
    finally:
        try:
            client.close()
        except:
            pass


if __name__ == "__main__":
    print("🏥 Migration du système d'analyse médicale")
    print("=" * 50)
    
    # Demander confirmation
    reponse = input("Voulez-vous lancer la migration ? (oui/non): ").lower()
    
    if reponse in ['oui', 'o', 'yes', 'y']:
        if run_migration():
            verification_post_migration()
        else:
            print("❌ Migration échouée")
    else:
        print("❌ Migration annulée")