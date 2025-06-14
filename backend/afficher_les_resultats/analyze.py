# from flask import Blueprint, request, jsonify, current_app
# from bson import ObjectId
# from datetime import datetime
# from auth.utils import token_required
# import os
# import cv2
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import traceback
# import logging

# analyze_bp = Blueprint('analyze', __name__)

# # Variables globales pour le modèle
# pneumonia_model = None
# MODEL_PATH = None

# def load_pneumonia_model():
#     """Charge le modèle de pneumonie"""
#     global pneumonia_model, MODEL_PATH
    
#     if pneumonia_model is not None:
#         return pneumonia_model
    
#     try:
#         # Chemins possibles du modèle (ajustez selon votre structure)
#         possible_paths = [
#             os.path.join(os.path.dirname(__file__), '..', 'ia', 'models', 'pneumonia_model_best.h5'),
#             os.path.join(os.path.dirname(__file__), '..', 'models', 'pneumonia_model_best.h5'),
#             os.path.join(os.getcwd(), 'ia', 'models', 'pneumonia_model_best.h5'),
#             os.path.join(os.getcwd(), 'models', 'pneumonia_model_best.h5')
#         ]
        
#         for path in possible_paths:
#             if os.path.exists(path):
#                 MODEL_PATH = path
#                 break
        
#         if MODEL_PATH is None:
#             raise FileNotFoundError("Modèle de pneumonie non trouvé")
        
#         print(f"Chargement du modèle depuis: {MODEL_PATH}")
#         pneumonia_model = load_model(MODEL_PATH)
#         print("✅ Modèle de pneumonie chargé avec succès")
#         return pneumonia_model
        
#     except Exception as e:
#         print(f"❌ Erreur lors du chargement du modèle: {str(e)}")
#         raise e

# def preprocess_image_for_ai(image_path):
#     """Prétraite l'image pour l'IA (identique au GUI)"""
#     try:
#         # Lire l'image
#         img = cv2.imread(image_path)
#         if img is None:
#             raise ValueError(f"Impossible de lire l'image: {image_path}")
        
#         # Convertir en niveaux de gris
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Appliquer CLAHE
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#         clahe_img = clahe.apply(gray)
        
#         # Redimensionner à 224x224
#         img_size = 224
#         resized = cv2.resize(clahe_img, (img_size, img_size))
        
#         # Normaliser
#         normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
        
#         # Convertir en 3 canaux
#         img_3channels = cv2.cvtColor(normalized, cv2.COLOR_GRAY2RGB)
        
#         # Normaliser les pixels à [-1, 1]
#         img_3channels = img_3channels / 127.5 - 1
        
#         # Ajouter dimension batch
#         img_3channels = np.expand_dims(img_3channels, axis=0)
        
#         return img_3channels
        
#     except Exception as e:
#         raise Exception(f"Erreur prétraitement image: {str(e)}")

# def predict_pneumonia(image_path):
#     """Prédit la pneumonie sur une image"""
#     try:
#         # Charger le modèle
#         model = load_pneumonia_model()
        
#         # Prétraiter l'image
#         preprocessed_img = preprocess_image_for_ai(image_path)
        
#         # Faire la prédiction
#         prediction = model.predict(preprocessed_img)
        
#         # Analyser les résultats
#         classes = ['NORMAL', 'PNEUMONIA']
#         class_idx = np.argmax(prediction[0])
#         confidence = float(prediction[0][class_idx])
#         predicted_class = classes[class_idx]
        
#         # Probabilités pour les deux classes
#         normal_prob = float(prediction[0][0])
#         pneumonia_prob = float(prediction[0][1])
        
#         # Déterminer la sévérité si c'est une pneumonie
#         severity = "Normal"
#         recommendations = []
        
#         if predicted_class == "PNEUMONIA":
#             if confidence > 0.9:
#                 severity = "Élevée"
#                 recommendations = [
#                     "Consultation d'urgence recommandée",
#                     "Traitement antibiotique probable",
#                     "Surveillance rapprochée nécessaire"
#                 ]
#             elif confidence > 0.7:
#                 severity = "Modérée"
#                 recommendations = [
#                     "Consultation pneumologue dans les 24h",
#                     "Examens complémentaires à envisager",
#                     "Traitement symptomatique"
#                 ]
#             else:
#                 severity = "Faible"
#                 recommendations = [
#                     "Surveillance clinique",
#                     "Contrôle dans 48-72h",
#                     "Réévaluation si aggravation"
#                 ]
#         else:
#             recommendations = [
#                 "Résultat normal",
#                 "Surveillance habituelle",
#                 "Consultation si symptômes persistent"
#             ]
        
#         return {
#             'prediction': predicted_class,
#             'confidence': confidence,
#             'details': {
#                 'probabilite_normale': normal_prob,
#                 'probabilite_pneumonie': pneumonia_prob,
#                 'severite': severity,
#                 'recommendations': recommendations,
#                 'zone_affectee': 'Analyse globale' if predicted_class == "PNEUMONIA" else 'Aucune',
#                 'modele_utilise': 'CNN Pneumonie v1.0'
#             }
#         }
        
#     except Exception as e:
#         raise Exception(f"Erreur prédiction pneumonie: {str(e)}")

# @analyze_bp.route('/api/analyze/<image_id>', methods=['POST'])
# @token_required
# def analyze_image(user_id, image_id):
#     """Lance l'analyse IA d'une image médicale"""
#     try:
#         db = current_app.config['db']
        
#         # Vérifier que l'image existe et appartient à l'utilisateur
#         image_doc = db.images.find_one({
#             '_id': ObjectId(image_id),
#             'utilisateurId': ObjectId(user_id)
#         })
        
#         if not image_doc:
#             return jsonify({'error': 'Image non trouvée'}), 404
            
#         # Vérifier si une analyse existe déjà
#         existing_analysis = db.analyses.find_one({'imageId': ObjectId(image_id)})
#         if existing_analysis:
#             return jsonify({
#                 'message': 'Analyse déjà effectuée',
#                 'analysis': {
#                     'id': str(existing_analysis['_id']),
#                     'resultat': existing_analysis['resultat'],
#                     'confiance': existing_analysis['confiance'],
#                     'details': existing_analysis.get('details', {}),
#                     'patient': existing_analysis.get('patient', {}),
#                     'dateAnalyse': existing_analysis['dateAnalyse'].isoformat()
#                 }
#             }), 200
        
#         # Vérifier que le fichier existe
#         image_path = image_doc['filepath']
#         if not os.path.exists(image_path):
#             return jsonify({'error': 'Fichier image non trouvé sur le serveur'}), 404
            
#         # Mettre à jour le statut de l'image
#         db.images.update_one(
#             {'_id': ObjectId(image_id)},
#             {'$set': {'statut': 'analyse'}}
#         )
        
#         print(f"🔍 Début de l'analyse IA pour l'image: {image_path}")
        
#         # Faire l'analyse IA
#         ia_result = predict_pneumonia(image_path)
        
#         print(f"✅ Analyse terminée: {ia_result['prediction']} (confiance: {ia_result['confidence']:.2f})")
        
#         # Enregistrer les résultats de l'analyse
#         analysis_data = {
#             'imageId': ObjectId(image_id),
#             'utilisateurId': ObjectId(user_id),
#             'patient': image_doc['patient'],
#             'resultat': ia_result['prediction'],
#             'confiance': ia_result['confidence'],
#             'details': ia_result.get('details', {}),
#             'dateAnalyse': datetime.utcnow(),
#             'statut': 'termine'
#         }
        
#         result = db.analyses.insert_one(analysis_data)
        
#         # Mettre à jour le statut de l'image
#         db.images.update_one(
#             {'_id': ObjectId(image_id)},
#             {'$set': {'statut': 'termine'}}
#         )
        
#         return jsonify({
#             'message': 'Analyse terminée avec succès',
#             'analysis': {
#                 'id': str(result.inserted_id),
#                 'resultat': ia_result['prediction'],
#                 'confiance': ia_result['confidence'],
#                 'details': ia_result.get('details', {}),
#                 'patient': image_doc['patient'],
#                 'dateAnalyse': analysis_data['dateAnalyse'].isoformat()
#             }
#         }), 200
        
#     except Exception as e:
#         # En cas d'erreur, remettre le statut à en_attente
#         try:
#             db.images.update_one(
#                 {'_id': ObjectId(image_id)},
#                 {'$set': {'statut': 'en_attente'}}
#             )
#         except:
#             pass
            
#         print(f"❌ Erreur analyse IA: {str(e)}")
#         print(traceback.format_exc())
#         current_app.logger.error(f'Erreur analyse IA: {str(e)}')
#         return jsonify({'error': f'Erreur lors de l\'analyse: {str(e)}'}), 500

# @analyze_bp.route('/api/analyses/<user_id>', methods=['GET'])
# @token_required
# def get_user_analyses(current_user_id, user_id):
#     """Récupère toutes les analyses d'un utilisateur"""
#     try:
#         db = current_app.config['db']
        
#         # Vérifier les permissions
#         if current_user_id != user_id:
#             user = db.users.find_one({'_id': ObjectId(current_user_id)})
#             if not user or user.get('role') != 'admin':
#                 return jsonify({'error': 'Accès non autorisé'}), 403
        
#         # Récupérer les analyses
#         analyses = list(db.analyses.find(
#             {'utilisateurId': ObjectId(user_id)}
#         ).sort('dateAnalyse', -1))
        
#         # Convertir ObjectId en string et enrichir les données
#         for analysis in analyses:
#             analysis['_id'] = str(analysis['_id'])
#             analysis['imageId'] = str(analysis['imageId'])
#             analysis['utilisateurId'] = str(analysis['utilisateurId'])
            
#             # Récupérer les informations de l'image associée
#             image_info = db.images.find_one({'_id': ObjectId(analysis['imageId'])})
#             if image_info:
#                 analysis['image_filename'] = image_info.get('filename', 'Non disponible')
            
#         return jsonify({
#             'analyses': analyses,
#             'count': len(analyses)
#         }), 200
        
#     except Exception as e:
#         current_app.logger.error(f'Erreur récupération analyses: {str(e)}')
#         return jsonify({'error': 'Erreur lors de la récupération des analyses'}), 500

# @analyze_bp.route('/api/save-analysis', methods=['POST'])
# @token_required
# def save_analysis(user_id):
#     """Sauvegarde finale de l'analyse avec notes du médecin"""
#     try:
#         db = current_app.config['db']
#         data = request.get_json()
        
#         analysis_id = data.get('analysisId')
#         notes_medecin = data.get('notes', '')
#         diagnostic_final = data.get('diagnostic', '')
        
#         if not analysis_id:
#             return jsonify({'error': 'ID d\'analyse requis'}), 400
            
#         # Mettre à jour l'analyse
#         result = db.analyses.update_one(
#             {
#                 '_id': ObjectId(analysis_id),
#                 'utilisateurId': ObjectId(user_id)
#             },
#             {
#                 '$set': {
#                     'notesMedecin': notes_medecin,
#                     'diagnosticFinal': diagnostic_final,
#                     'dateSauvegarde': datetime.utcnow(),
#                     'statut': 'sauvegarde'
#                 }
#             }
#         )
        
#         if result.matched_count == 0:
#             return jsonify({'error': 'Analyse non trouvée'}), 404
            
#         return jsonify({
#             'message': 'Analyse sauvegardée avec succès'
#         }), 200
        
#     except Exception as e:
#         current_app.logger.error(f'Erreur sauvegarde analyse: {str(e)}')
#         return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500

# @analyze_bp.route('/api/model-status', methods=['GET'])
# @token_required
# def get_model_status(user_id):
#     """Vérifie le statut du modèle IA"""
#     try:
#         model = load_pneumonia_model()
#         return jsonify({
#             'status': 'active',
#             'model_path': MODEL_PATH,
#             'message': 'Modèle IA prêt'
#         }), 200
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': f'Erreur modèle: {str(e)}'
#         }), 500

# # Configuration du logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Simulateur d'IA (remplacez par votre modèle réel)
# def analyser_image_medicale(chemin_image, donnees_patient):
#     """
#     Analyse une image médicale et retourne un diagnostic
    
#     Args:
#         chemin_image (str): Chemin vers le fichier image
#         donnees_patient (dict): Informations du patient
        
#     Returns:
#         dict: Résultats de l'analyse
#     """
#     try:
#         debut_analyse = time.time()
#         logger.info(f"🔍 Début analyse pour patient: {donnees_patient.get('nom', 'Inconnu')}")
        
#         # Vérifier que le fichier existe
#         if not os.path.exists(chemin_image):
#             logger.error(f"❌ Fichier non trouvé: {chemin_image}")
#             return None
            
#         # Charger et préprocesser l'image
#         image_analysee = preprocesser_image(chemin_image)
#         if image_analysee is None:
#             logger.error("❌ Erreur lors du préprocessing")
#             return None
            
#         # Simulation d'analyse IA (remplacez par votre modèle)
#         resultats = simuler_analyse_ia(image_analysee, donnees_patient)
        
#         # Calculer le temps d'analyse
#         temps_analyse = time.time() - debut_analyse
#         resultats['temps_analyse'] = round(temps_analyse, 2)
#         resultats['version_modele'] = "1.0.0"
#         resultats['algorithme'] = "CNN_ResNet50"
        
#         logger.info(f"✅ Analyse terminée en {temps_analyse:.2f}s - Résultat: {resultats['resultat']}")
        
#         return resultats
        
#     except Exception as e:
#         logger.error(f"❌ Erreur lors de l'analyse: {str(e)}")
#         return None


# def preprocesser_image(chemin_image):
#     """
#     Préprocess l'image pour l'analyse IA
#     """
#     try:
#         logger.info("📸 Préprocessing de l'image...")
        
#         # Charger l'image
#         if chemin_image.lower().endswith('.dcm'):
#             # Traitement DICOM (nécessite pydicom)
#             try:
#                 import pydicom
#                 ds = pydicom.dcmread(chemin_image)
#                 image_array = ds.pixel_array
#                 # Normaliser l'image DICOM
#                 image = Image.fromarray(image_array).convert('RGB')
#             except ImportError:
#                 logger.warning("⚠️ pydicom non installé, traitement DICOM limité")
#                 return None
#         else:
#             # Images standard (PNG, JPG, JPEG)
#             image = Image.open(chemin_image).convert('RGB')
        
#         # Redimensionner à 224x224 (standard pour les modèles CNN)
#         image = image.resize((224, 224))
        
#         # Convertir en array numpy
#         image_array = np.array(image)
        
#         # Normalisation
#         image_array = image_array.astype(np.float32) / 255.0
        
#         logger.info("✅ Préprocessing terminé")
#         return image_array
        
#     except Exception as e:
#         logger.error(f"❌ Erreur préprocessing: {str(e)}")
#         return None


# def simuler_analyse_ia(image_array, donnees_patient):
#     """
#     Simule l'analyse IA - REMPLACEZ PAR VOTRE MODÈLE RÉEL
#     """
#     try:
#         logger.info("🤖 Simulation de l'analyse IA...")
        
#         # Simulation basée sur des facteurs aléatoires mais cohérents
#         # Dans un vrai cas, vous utiliseriez votre modèle entraîné
        
#         # Facteurs influençant le diagnostic (simulation)
#         age = donnees_patient.get('age', 30)
#         symptomes = donnees_patient.get('symptomes', '').lower()
        
#         # Analyse de texture simple de l'image
#         moyenne_pixels = np.mean(image_array)
#         variance_pixels = np.var(image_array)
        
#         # Logique de simulation (remplacez par votre modèle)
#         score_pneumonie = 0.0
        
#         # Facteurs d'âge
#         if age > 65 or age < 2:
#             score_pneumonie += 0.2
        
#         # Facteurs symptomatiques
#         symptomes_pneumonie = ['fièvre', 'toux', 'difficulté', 'respir', 'douleur', 'thorax']
#         for symptome in symptomes_pneumonie:
#             if symptome in symptomes:
#                 score_pneumonie += 0.15
                
#         # Analyse d'image simulée
#         if moyenne_pixels < 0.3:  # Image sombre = zones suspectes
#             score_pneumonie += 0.3
#         if variance_pixels > 0.1:  # Forte variance = irrégularités
#             score_pneumonie += 0.2
            
#         # Ajouter un facteur aléatoire contrôlé
#         import random
#         random.seed(hash(donnees_patient.get('cin', '')) % 1000)  # Reproductible par patient
#         facteur_aleatoire = random.uniform(-0.1, 0.1)
#         score_pneumonie += facteur_aleatoire
        
#         # Limiter le score entre 0 et 1
#         score_pneumonie = max(0.0, min(1.0, score_pneumonie))
        
#         # Déterminer le résultat
#         seuil_diagnostic = 0.5
#         resultat = "PNEUMONIA" if score_pneumonie > seuil_diagnostic else "NORMAL"
#         confiance = score_pneumonie if resultat == "PNEUMONIA" else (1.0 - score_pneumonie)
        
#         # Générer les détails
#         details = generer_details_diagnostic(resultat, score_pneumonie, donnees_patient)
        
#         return {
#             'resultat': resultat,
#             'confiance': round(confiance, 3),
#             'probabilites': {
#                 'pneumonie': round(score_pneumonie, 3),
#                 'normale': round(1.0 - score_pneumonie, 3)
#             },
#             'details': details,
#             'recommandations': generer_recommandations(resultat, confiance, donnees_patient),
#             'metadata': {
#                 'moyenne_pixels': round(moyenne_pixels, 3),
#                 'variance_pixels': round(variance_pixels, 3)
#             }
#         }
        
#     except Exception as e:
#         logger.error(f"❌ Erreur simulation IA: {str(e)}")
#         return None


# def generer_details_diagnostic(resultat, score, donnees_patient):
#     """
#     Génère les détails du diagnostic
#     """
#     details = {}
    
#     if resultat == "PNEUMONIA":
#         if score > 0.8:
#             details['severite'] = "Élevée"
#         elif score > 0.6:
#             details['severite'] = "Modérée"
#         else:
#             details['severite'] = "Légère"
            
#         # Zones affectées simulées
#         zones = ["Lobe inférieur droit", "Lobe supérieur gauche", "Lobe moyen", "Bilatérale"]
#         import random
#         random.seed(hash(donnees_patient.get('cin', '')) % 100)
#         details['zone_affectee'] = random.choice(zones)
        
#     else:
#         details['severite'] = "Aucune"
#         details['zone_affectee'] = "Aucune zone suspecte détectée"
    
#     return details


# def generer_recommandations(resultat, confiance, donnees_patient):
#     """
#     Génère des recommandations médicales
#     """
#     recommandations = []
    
#     if resultat == "PNEUMONIA":
#         if confiance > 0.8:
#             recommandations.extend([
#                 "Consultation médicale urgente recommandée",
#                 "Examens complémentaires conseillés (analyses sanguines)",
#                 "Surveillance étroite des symptômes respiratoires"
#             ])
#         else:
#             recommandations.extend([
#                 "Consultation médicale dans les 24-48h",
#                 "Surveillance des symptômes",
#                 "Repos et hydratation"
#             ])
            
#         # Recommandations spécifiques à l'âge
#         age = donnees_patient.get('age', 30)
#         if age > 65:
#             recommandations.append("Attention particulière requise (patient âgé)")
#         elif age < 5:
#             recommandations.append("Surveillance pédiatrique recommandée")
            
#     else:
#         recommandations.extend([
#             "Résultats normaux - pas d'anomalie détectée",
#             "Continuer la surveillance si symptômes persistent",
#             "Consultation si aggravation des symptômes"
#         ])
    
#     recommandations.append("⚠️ Cette analyse IA est un outil d'aide au diagnostic - Consultation médicale requise")
    
#     return recommandations


# def obtenir_statistiques_modele():
#     """
#     Retourne les statistiques du modèle (pour le monitoring)
#     """
#     return {
#         'version': "1.0.0",
#         'derniere_mise_a_jour': "2024-12-01",
#         'precision_estimee': 0.92,
#         'rappel_estime': 0.89,
#         'f1_score_estime': 0.90,
#         'nombre_echantillons_entrainement': 10000,
#         'types_supports': ['.png', '.jpg', '.jpeg', '.dcm']
#     }


# if __name__ == "__main__":
#     # Test du module
#     print("🧪 Test du module d'analyse IA...")
    
#     # Données de test
#     donnees_test = {
#         'nom': 'Patient Test',
#         'age': 45,
#         'cin': 'AB123456',
#         'symptomes': 'toux sèche, fièvre, difficulté à respirer',
#         'type_examen': 'radiographie'
#     }
    
#     # Note: Pour tester, vous devez avoir une image
#     # resultat = analyser_image_medicale('path/to/test/image.jpg', donnees_test)
#     # print("Résultat:", resultat)
    
#     print("✅ Module chargé avec succès")
#     print("Stats modèle:", obtenir_statistiques_modele())






# # analyze.py - Version améliorée
# from flask import Blueprint, request, jsonify, current_app
# from bson import ObjectId
# from datetime import datetime
# from auth.utils import token_required
# import os
# import cv2
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import traceback
# import logging

# analyze_bp = Blueprint('analyze', __name__)

# # Variables globales pour le modèle
# pneumonia_model = None
# MODEL_PATH = None

# def load_pneumonia_model():
#     """Charge le modèle de pneumonie avec gestion d'erreurs améliorée"""
#     global pneumonia_model, MODEL_PATH
    
#     if pneumonia_model is not None:
#         return pneumonia_model
    
#     try:
#         # Chemins possibles du modèle
#         possible_paths = [
#             os.path.join(os.path.dirname(__file__), '..', 'ia', 'models', 'pneumonia_model_best.h5'),
#             os.path.join(os.path.dirname(__file__), '..', 'models', 'pneumonia_model_best.h5'),
#             os.path.join(os.getcwd(), 'ia', 'models', 'pneumonia_model_best.h5'),
#             os.path.join(os.getcwd(), 'models', 'pneumonia_model_best.h5')
#         ]
        
#         for path in possible_paths:
#             if os.path.exists(path):
#                 MODEL_PATH = path
#                 break
        
#         if MODEL_PATH is None:
#             raise FileNotFoundError("Modèle de pneumonie non trouvé")
        
#         print(f"🔄 Chargement du modèle depuis: {MODEL_PATH}")
#         pneumonia_model = load_model(MODEL_PATH)
#         print("✅ Modèle de pneumonie chargé avec succès")
        
#         # Test du modèle avec une image factice
#         test_input = np.random.rand(1, 224, 224, 3)
#         test_prediction = pneumonia_model.predict(test_input, verbose=0)
#         print(f"✅ Test du modèle réussi, forme de sortie: {test_prediction.shape}")
        
#         return pneumonia_model
        
#     except Exception as e:
#         print(f"❌ Erreur lors du chargement du modèle: {str(e)}")
#         traceback.print_exc()
#         raise e

# def preprocess_image_for_ai(image_path):
#     """Prétraite l'image pour l'IA avec validation améliorée"""
#     try:
#         print(f"🖼️ Prétraitement de l'image: {image_path}")
        
#         # Vérifier que le fichier existe
#         if not os.path.exists(image_path):
#             raise FileNotFoundError(f"Fichier image non trouvé: {image_path}")
        
#         # Lire l'image
#         img = cv2.imread(image_path)
#         if img is None:
#             raise ValueError(f"Impossible de lire l'image: {image_path}")
        
#         print(f"📐 Image originale: {img.shape}")
        
#         # Convertir en niveaux de gris
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Appliquer CLAHE pour améliorer le contraste
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#         clahe_img = clahe.apply(gray)
        
#         # Redimensionner à 224x224
#         img_size = 224
#         resized = cv2.resize(clahe_img, (img_size, img_size))
        
#         # Normaliser
#         normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
        
#         # Convertir en 3 canaux
#         img_3channels = cv2.cvtColor(normalized, cv2.COLOR_GRAY2RGB)
        
#         # Normaliser les pixels à [-1, 1]
#         img_3channels = img_3channels / 127.5 - 1
        
#         # Ajouter dimension batch
#         img_3channels = np.expand_dims(img_3channels, axis=0)
        
#         print(f"✅ Image prétraitée: {img_3channels.shape}")
#         return img_3channels
        
#     except Exception as e:
#         print(f"❌ Erreur prétraitement image: {str(e)}")
#         raise Exception(f"Erreur prétraitement image: {str(e)}")

# def predict_pneumonia(image_path):
#     """Prédit la pneumonie sur une image avec gestion d'erreurs améliorée"""
#     try:
#         print(f"🔍 Début de la prédiction pour: {image_path}")
        
#         # Charger le modèle
#         model = load_pneumonia_model()
        
#         # Prétraiter l'image
#         preprocessed_img = preprocess_image_for_ai(image_path)
        
#         # Faire la prédiction
#         print("🤖 Exécution de la prédiction...")
#         prediction = model.predict(preprocessed_img, verbose=0)
#         print(f"📊 Prédiction brute: {prediction}")
        
#         # Analyser les résultats
#         classes = ['NORMAL', 'PNEUMONIA']
#         class_idx = np.argmax(prediction[0])
#         confidence = float(prediction[0][class_idx])
#         predicted_class = classes[class_idx]
        
#         # Probabilités pour les deux classes
#         normal_prob = float(prediction[0][0])
#         pneumonia_prob = float(prediction[0][1])
        
#         print(f"🎯 Résultat: {predicted_class} (confiance: {confidence:.3f})")
        
#         # Déterminer la sévérité et recommandations si c'est une pneumonie
#         severity = "Normal"
#         recommendations = []
        
#         if predicted_class == "PNEUMONIA":
#             if confidence >= 0.9:
#                 severity = "Élevée"
#                 recommendations = [
#                     "Consultation d'urgence recommandée",
#                     "Traitement antibiotique probable",
#                     "Surveillance rapprochée nécessaire"
#                 ]
#             elif confidence >= 0.7:
#                 severity = "Modérée"
#                 recommendations = [
#                     "Consultation pneumologue dans les 24h",
#                     "Examens complémentaires à envisager",
#                     "Traitement symptomatique"
#                 ]
#             else:
#                 severity = "Faible"
#                 recommendations = [
#                     "Surveillance clinique",
#                     "Contrôle dans 48-72h",
#                     "Réévaluation si aggravation"
#                 ]
#         else:
#             recommendations = [
#                 "Résultat normal",
#                 "Surveillance habituelle",
#                 "Consultation si symptômes persistent"
#             ]
        
#         result = {
#             'prediction': predicted_class,
#             'confidence': confidence,
#             'details': {
#                 'probabilite_normale': normal_prob,
#                 'probabilite_pneumonie': pneumonia_prob,
#                 'severite': severity,
#                 'recommendations': recommendations,
#                 'zone_affectee': 'Analyse globale' if predicted_class == "PNEUMONIA" else 'Aucune anomalie détectée',
#                 'modele_utilise': 'CNN Pneumonie v1.0'
#             }
#         }
        
#         print(f"✅ Analyse terminée avec succès")
#         return result
        
#     except Exception as e:
#         print(f"❌ Erreur prédiction pneumonie: {str(e)}")
#         traceback.print_exc()
#         raise Exception(f"Erreur prédiction pneumonie: {str(e)}")

# @analyze_bp.route('/api/analyze/<image_id>', methods=['POST'])
# @token_required
# def analyze_image(user_id, image_id):
#     """Lance l'analyse IA d'une image médicale avec logging amélioré"""
#     try:
#         db = current_app.config['db']
#         print(f"🚀 Début analyse pour image {image_id} par utilisateur {user_id}")
        
#         # Vérifier que l'image existe et appartient à l'utilisateur
#         image_doc = db.images.find_one({
#             '_id': ObjectId(image_id),
#             'utilisateurId': ObjectId(user_id)
#         })
        
#         if not image_doc:
#             print(f"❌ Image {image_id} non trouvée pour utilisateur {user_id}")
#             return jsonify({'error': 'Image non trouvée'}), 404
        
#         # Vérifier si une analyse existe déjà
#         existing_analysis = db.analyses.find_one({'imageId': ObjectId(image_id)})
#         if existing_analysis:
#             print(f"ℹ️ Analyse existante trouvée pour image {image_id}")
#             return jsonify({
#                 'message': 'Analyse déjà effectuée',
#                 'analysis': {
#                     'id': str(existing_analysis['_id']),
#                     'resultat': existing_analysis['resultat'],
#                     'confiance': existing_analysis['confiance'],
#                     'details': existing_analysis.get('details', {}),
#                     'patient': existing_analysis.get('patient', {}),
#                     'dateAnalyse': existing_analysis['dateAnalyse'].isoformat()
#                 }
#             }), 200
        
#         # Vérifier que le fichier existe
#         image_path = image_doc['filepath']
#         if not os.path.exists(image_path):
#             print(f"❌ Fichier image non trouvé: {image_path}")
#             return jsonify({'error': 'Fichier image non trouvé sur le serveur'}), 404
        
#         # Mettre à jour le statut de l'image
#         db.images.update_one(
#             {'_id': ObjectId(image_id)},
#             {'$set': {'statut': 'analyse'}}
#         )
        
#         print(f"🔍 Début de l'analyse IA pour l'image: {image_path}")
        
#         # Faire l'analyse IA
#         ia_result = predict_pneumonia(image_path)
        
#         print(f"✅ Analyse terminée: {ia_result['prediction']} (confiance: {ia_result['confidence']:.3f})")
        
#         # Enregistrer les résultats de l'analyse
#         analysis_data = {
#             'imageId': ObjectId(image_id),
#             'utilisateurId': ObjectId(user_id),
#             'patient': image_doc['patient'],
#             'resultat': ia_result['prediction'],
#             'confiance': ia_result['confidence'],
#             'details': ia_result.get('details', {}),
#             'dateAnalyse': datetime.utcnow(),
#             'statut': 'termine'
#         }
        
#         result = db.analyses.insert_one(analysis_data)
        
#         # Mettre à jour le statut de l'image
#         db.images.update_one(
#             {'_id': ObjectId(image_id)},
#             {'$set': {'statut': 'termine', 'analyseId': result.inserted_id}}
#         )
        
#         print(f"💾 Analyse sauvegardée avec ID: {result.inserted_id}")
        
#         return jsonify({
#             'message': 'Analyse terminée avec succès',
#             'analysis': {
#                 'id': str(result.inserted_id),
#                 'resultat': ia_result['prediction'],
#                 'confiance': ia_result['confidence'],
#                 'details': ia_result.get('details', {}),
#                 'patient': image_doc['patient'],
#                 'dateAnalyse': analysis_data['dateAnalyse'].isoformat()
#             }
#         }), 200
        
#     except Exception as e:
#         # En cas d'erreur, remettre le statut à en_attente
#         try:
#             db.images.update_one(
#                 {'_id': ObjectId(image_id)},
#                 {'$set': {'statut': 'en_attente'}}
#             )
#         except:
#             pass
        
#         error_msg = str(e)
#         print(f"❌ Erreur analyse IA: {error_msg}")
#         print(traceback.format_exc())
#         current_app.logger.error(f'Erreur analyse IA: {error_msg}')
        
#         return jsonify({'error': f'Erreur lors de l\'analyse: {error_msg}'}), 500

# # Route pour vérifier le statut du modèle
# @analyze_bp.route('/api/model/status', methods=['GET'])
# @token_required
# def model_status(user_id):
#     """Vérifie le statut du modèle IA"""
#     try:
#         global pneumonia_model, MODEL_PATH
        
#         status = {
#             'model_loaded': pneumonia_model is not None,
#             'model_path': MODEL_PATH,
#             'tensorflow_version': tf.__version__
#         }
        
#         if pneumonia_model is None:
#             try:
#                 load_pneumonia_model()
#                 status['model_loaded'] = True
#                 status['message'] = 'Modèle chargé avec succès'
#             except Exception as e:
#                 status['error'] = str(e)
#                 status['message'] = 'Erreur de chargement du modèle'
#         else:
#             status['message'] = 'Modèle déjà chargé'
            
#         return jsonify(status), 200
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500




from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from auth.utils import token_required
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import traceback
import logging
import base64

analyze_bp = Blueprint('analyze', __name__)

# Variables globales pour le modèle
pneumonia_model = None
MODEL_PATH = None

class GradCAM:
    def __init__(self, model, last_conv_layer_name=None):
        """Initialize GradCAM with a model"""
        self.model = model
        
        # Si le nom de la dernière couche convolutionnelle n'est pas fourni, la trouver automatiquement
        if last_conv_layer_name is None:
            for layer in reversed(model.layers):
                if 'conv' in layer.name:
                    last_conv_layer_name = layer.name
                    break
        
        if last_conv_layer_name is None:
            raise ValueError("Could not find a convolutional layer in the model")
            
        self.last_conv_layer_name = last_conv_layer_name
        self.grad_model = self._create_grad_model()
        
    def _create_grad_model(self):
        """Create a model that maps from the input image to conv layer outputs and the predicted class"""
        grad_model = tf.keras.models.Model(
            inputs=[self.model.inputs], 
            outputs=[
                self.model.get_layer(self.last_conv_layer_name).output, 
                self.model.output
            ]
        )
        return grad_model
        
    def generate_heatmap(self, img_array, class_idx=None):
        """Generate a heatmap for the specified class"""
        with tf.GradientTape() as tape:
            last_conv_output, preds = self.grad_model(img_array)
            if class_idx is None:
                class_idx = tf.argmax(preds[0])
            class_channel = preds[:, class_idx]
            
        # Calculer le gradient de la classe par rapport à la sortie de la couche conv
        grads = tape.gradient(class_channel, last_conv_output)
        
        # Vector of mean intensity of gradients over feature map channels
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Multiplier chaque canal par l'importance de ce canal
        last_conv_output = last_conv_output[0]
        heatmap = last_conv_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normaliser la heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()
        
    def overlay_heatmap(self, img, heatmap, alpha=0.5):
        """Overlay the heatmap on the original image"""
        # Redimensionner la heatmap à la taille de l'image originale
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        
        # Convertir la heatmap en RGB
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Superposer la heatmap sur l'image originale
        superimposed_img = heatmap * alpha + img
        superimposed_img = np.uint8(np.clip(superimposed_img, 0, 255))
        
        return superimposed_img, heatmap

def load_pneumonia_model():
    """Charge le modèle de pneumonie"""
    global pneumonia_model, MODEL_PATH
    if pneumonia_model is not None:
        return pneumonia_model
    
    try:
        # Chemins possibles du modèle
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'ia', 'models', 'pneumonia_model_best.h5'),
            os.path.join(os.path.dirname(__file__), '..', 'models', 'pneumonia_model_best.h5'),
            os.path.join(os.getcwd(), 'ia', 'models', 'pneumonia_model_best.h5'),
            os.path.join(os.getcwd(), 'models', 'pneumonia_model_best.h5')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                MODEL_PATH = path
                break
        
        if MODEL_PATH is None:
            raise FileNotFoundError("Modèle de pneumonie non trouvé")
        
        print(f"Chargement du modèle depuis: {MODEL_PATH}")
        pneumonia_model = load_model(MODEL_PATH)
        print("✅ Modèle de pneumonie chargé avec succès")
        return pneumonia_model
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {str(e)}")
        raise e

def preprocess_image_for_ai(image_path):
    """Prétraite l'image pour l'IA"""
    try:
        # Lire l'image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossible de lire l'image: {image_path}")
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Appliquer CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(gray)
        
        # Redimensionner à 224x224
        img_size = 224
        resized = cv2.resize(clahe_img, (img_size, img_size))
        
        # Normaliser
        normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
        
        # Convertir en 3 canaux
        img_3channels = cv2.cvtColor(normalized, cv2.COLOR_GRAY2RGB)
        
        # Normaliser les pixels à [-1, 1]
        img_3channels = img_3channels / 127.5 - 1
        
        # Ajouter dimension batch
        img_3channels = np.expand_dims(img_3channels, axis=0)
        
        return img_3channels, img
        
    except Exception as e:
        raise Exception(f"Erreur prétraitement image: {str(e)}")

def predict_pneumonia(image_path):
    """Prédit la pneumonie sur une image et génère la heatmap"""
    try:
        # Charger le modèle
        model = load_pneumonia_model()
        
        # Prétraiter l'image
        preprocessed_img, original_img = preprocess_image_for_ai(image_path)
        
        # Faire la prédiction
        prediction = model.predict(preprocessed_img)
        
        # Analyser les résultats
        classes = ['NORMAL', 'PNEUMONIA']
        class_idx = np.argmax(prediction[0])
        confidence = float(prediction[0][class_idx])
        predicted_class = classes[class_idx]
        
        # Probabilités pour les deux classes
        normal_prob = float(prediction[0][0])
        pneumonia_prob = float(prediction[0][1])
        
        # Générer la heatmap
        gradcam = GradCAM(model)
        heatmap = gradcam.generate_heatmap(preprocessed_img, class_idx)
        superimposed_img, raw_heatmap = gradcam.overlay_heatmap(original_img, heatmap)
        
        # Convertir les images en base64 pour l'envoi
        def image_to_base64(img):
            _, buffer = cv2.imencode('.png', img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"
        
        heatmap_base64 = image_to_base64(superimposed_img)
        
        # Déterminer la sévérité si c'est une pneumonie
        severity = "Normal"
        recommendations = []
        
        if predicted_class == "PNEUMONIA":
            if confidence >= 0.9:
                severity = "Élevée"
                recommendations = [
                    "Consultation d'urgence recommandée",
                    "Traitement antibiotique probable",
                    "Surveillance rapprochée nécessaire"
                ]
            elif confidence >= 0.7:
                severity = "Modérée"
                recommendations = [
                    "Consultation pneumologue dans les 24h",
                    "Examens complémentaires à envisager",
                    "Traitement symptomatique"
                ]
            else:
                severity = "Faible"
                recommendations = [
                    "Surveillance clinique",
                    "Contrôle dans 48-72h",
                    "Réévaluation si aggravation"
                ]
        else:
            recommendations = [
                "Résultat normal",
                "Surveillance habituelle",
                "Consultation si symptômes persistent"
            ]
        
        return {
            'prediction': predicted_class,
            'confidence': confidence,
            'heatmap': heatmap_base64,
            'details': {
                'probabilite_normale': normal_prob,
                'probabilite_pneumonie': pneumonia_prob,
                'severite': severity,
                'recommendations': recommendations,
                'zone_affectee': 'Analyse globale' if predicted_class == "PNEUMONIA" else 'Normal',
                'modele_utilise': 'CNN Pneumonie v1.0'
            }
        }
        
    except Exception as e:
        raise Exception(f"Erreur prédiction pneumonie: {str(e)}")

@analyze_bp.route('/api/analyze/<image_id>', methods=['POST'])
@token_required
def analyze_image(user_id, image_id):
    """Lance l'analyse IA d'une image médicale"""
    try:
        db = current_app.config['db']
        
        # Vérifier que l'image existe et appartient à l'utilisateur
        image_doc = db.images.find_one({
            '_id': ObjectId(image_id),
            'utilisateurId': ObjectId(user_id)
        })
        
        if not image_doc:
            return jsonify({'error': 'Image non trouvée'}), 404
        
        # Vérifier si une analyse existe déjà
        existing_analysis = db.analyses.find_one({'imageId': ObjectId(image_id)})
        if existing_analysis:
            return jsonify({
                'message': 'Analyse déjà effectuée',
                'analysis': {
                    'id': str(existing_analysis['_id']),
                    'resultat': existing_analysis['resultat'],
                    'confiance': existing_analysis['confiance'],
                    'heatmap': existing_analysis.get('heatmap', ''),
                    'details': existing_analysis.get('details', {}),
                    'patient': existing_analysis.get('patient', {}),
                    'dateAnalyse': existing_analysis['dateAnalyse'].isoformat()
                }
            }), 200
        
        # Vérifier que le fichier existe
        image_path = image_doc['filepath']
        if not os.path.exists(image_path):
            return jsonify({'error': 'Fichier image non trouvé sur le serveur'}), 404
        
        # Mettre à jour le statut de l'image
        db.images.update_one(
            {'_id': ObjectId(image_id)},
            {'$set': {'statut': 'analyse'}}
        )
        
        print(f"🔍 Début de l'analyse IA pour l'image: {image_path}")
        
        # Faire l'analyse IA
        ia_result = predict_pneumonia(image_path)
        
        print(f"✅ Analyse terminée: {ia_result['prediction']} (confiance: {ia_result['confidence']:.2f})")
        
        # Enregistrer les résultats de l'analyse
        analysis_data = {
            'imageId': ObjectId(image_id),
            'utilisateurId': ObjectId(user_id),
            'patient': image_doc['patient'],
            'resultat': ia_result['prediction'],
            'confiance': ia_result['confidence'],
            'heatmap': ia_result['heatmap'],
            'details': ia_result.get('details', {}),
            'dateAnalyse': datetime.utcnow(),
            'statut': 'termine'
        }
        
        result = db.analyses.insert_one(analysis_data)
        
        # Mettre à jour le statut de l'image
        db.images.update_one(
            {'_id': ObjectId(image_id)},
            {'$set': {'statut': 'termine'}}
        )
        
        return jsonify({
            'message': 'Analyse terminée avec succès',
            'analysis': {
                'id': str(result.inserted_id),
                'resultat': ia_result['prediction'],
                'confiance': ia_result['confidence'],
                'heatmap': ia_result['heatmap'],
                'details': ia_result.get('details', {}),
                'patient': image_doc['patient'],
                'dateAnalyse': analysis_data['dateAnalyse'].isoformat()
            }
        }), 200
        
    except Exception as e:
        # En cas d'erreur, remettre le statut à en_attente
        try:
            db.images.update_one(
                {'_id': ObjectId(image_id)},
                {'$set': {'statut': 'en_attente'}}
            )
        except:
            pass
        
        print(f"❌ Erreur analyse IA: {str(e)}")
        print(traceback.format_exc())
        current_app.logger.error(f'Erreur analyse IA: {str(e)}')
        return jsonify({'error': f'Erreur lors de l\'analyse: {str(e)}'}), 500