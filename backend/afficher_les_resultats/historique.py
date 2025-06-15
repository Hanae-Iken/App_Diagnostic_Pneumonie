from flask import Blueprint, jsonify, current_app, request
from auth.utils import token_required
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import base64
import os

history_bp = Blueprint('history_bp', __name__)

@history_bp.route('/api/history', methods=['GET'])  # Changé de '/history' à '/api/history'
@token_required
def get_history(user_id):
    try:
        db = current_app.config["db"]
        
        # Récupérer le filtre de temps depuis les paramètres
        time_filter = request.args.get('filter', 'all')
        
        # Calculer la date de début selon le filtre
        date_filter = {}
        if time_filter == 'day':
            start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            date_filter = {'dateAnalyse': {'$gte': start_date}}
        elif time_filter == 'week':
            start_date = datetime.utcnow() - timedelta(days=7)
            date_filter = {'dateAnalyse': {'$gte': start_date}}
        elif time_filter == 'month':
            start_date = datetime.utcnow() - timedelta(days=30)
            date_filter = {'dateAnalyse': {'$gte': start_date}}
            
        # Requête pour récupérer les analyses avec les images
        pipeline = [
            {
                '$match': {
                    'utilisateurId': ObjectId(user_id),
                    **date_filter
                }
            },
            {
                '$lookup': {
                    'from': 'images',
                    'localField': 'imageId',
                    'foreignField': '_id',
                    'as': 'image_info'
                }
            },
            {
                '$sort': {'dateAnalyse': -1}
            }
        ]
        
        analyses = list(db.analyses.aggregate(pipeline))
        print(f"Analyses trouvées: {len(analyses)}")  # Debug
        
        # Formatter les données pour le frontend
        historique = []
        for analyse in analyses:
            try:
                image_info = analyse.get('image_info', [{}])[0]
                
                # Lire l'image et la convertir en base64
                image_base64 = None
                if image_info.get('filepath') and os.path.exists(image_info['filepath']):
                    try:
                        with open(image_info['filepath'], 'rb') as img_file:
                            image_data = img_file.read()
                            image_base64 = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
                    except Exception as e:
                        print(f"Erreur lecture image: {e}")
                
                # Vérifier que les champs obligatoires existent
                patient_data = analyse.get('patient', {})
                if not patient_data:
                    print(f"Pas de données patient pour l'analyse {analyse['_id']}")
                    continue
                
                item = {
                    'id': str(analyse['_id']),
                    'patient': {
                        'nomComplet': patient_data.get('nomComplet', 'Nom inconnu'),
                        'age': patient_data.get('age', 0),
                        'cin': patient_data.get('cin', 'Non renseigné'),
                        'symptomes': patient_data.get('symptomes', 'Non renseignés')
                    },
                    'date': analyse['dateAnalyse'].strftime('%d/%m/%Y'),
                    'time': analyse['dateAnalyse'].strftime('%H:%M'),
                    'resultat': analyse.get('resultat', 'Inconnu'),
                    'confiance': round(analyse.get('confiance', 0) * 100, 1),
                    'image': image_base64,
                    'details': analyse.get('details', {}),
                    'heatmap': analyse.get('heatmap', '')
                }
                historique.append(item)
                
            except Exception as e:
                print(f"Erreur traitement analyse {analyse.get('_id', 'unknown')}: {e}")
                continue
            
        print(f"Historique formaté: {len(historique)} éléments")  # Debug
        
        return jsonify({
            'historique': historique,
            'total': len(historique)
        }), 200
        
    except Exception as e:
        print(f"Erreur historique: {e}")
        current_app.logger.error(f'Erreur historique: {str(e)}')
        return jsonify({'error': 'Erreur lors de la récupération de l\'historique'}), 500