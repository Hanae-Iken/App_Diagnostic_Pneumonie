from flask import Blueprint, jsonify, current_app, request
from bson import ObjectId
from auth.utils import token_required

patients_bp = Blueprint('patients_bp', __name__)

@patients_bp.route('/patients', methods=['GET'])
@token_required
def get_patients(user_id):
    try:
        db = current_app.config['db']
        
        # Récupérer tous les patients de l'utilisateur connecté
        images = db.images.find(
            {'utilisateurId': ObjectId(user_id)},
            {
                'patient.nomComplet': 1,
                'patient.age': 1, 
                'patient.cin': 1,
                'dateUpload': 1,
                'statut': 1,
                '_id': 1
            }
        ).sort('dateUpload', -1)  # Tri par date décroissante
        
        patients_list = []
        seen_patients = set()  # Pour éviter les doublons
        
        for image in images:
            patient = image.get('patient', {})
            cin = patient.get('cin', '')
            
            # Éviter les doublons basés sur le CIN
            if cin and cin not in seen_patients:
                seen_patients.add(cin)
                
                # Déterminer le genre basé sur le prénom (simple heuristique)
                nom = patient.get('nomComplet', '')
                gender = 'F' if any(x in nom.lower() for x in ['fatima', 'khadija', 'aicha', 'zineb', 'leila', 'amina']) else 'M'
                
                patients_list.append({
                    'id': str(image['_id']),
                    'name': patient.get('nomComplet', 'N/A'),
                    'age': patient.get('age', 0),
                    'gender': gender,
                    'cin': cin,
                    'lastVisit': image.get('dateUpload', '').strftime('%d/%m/%Y') if image.get('dateUpload') else 'N/A',
                    'status': 'active' if image.get('statut') != 'termine' else 'inactive'
                })
        
        return jsonify({
            'patients': patients_list,
            'total': len(patients_list)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Erreur récupération patients: {str(e)}')
        return jsonify({'error': 'Erreur lors de la récupération des patients'}), 500