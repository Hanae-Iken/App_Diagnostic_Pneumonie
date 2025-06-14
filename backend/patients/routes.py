from flask import Blueprint, jsonify, current_app
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
        ).sort('dateUpload', -1)
        
        patients_list = []
        seen_patients = set()
        
        for image in images:
            patient = image.get('patient', {})
            cin = patient.get('cin', '')
            
            if cin and cin not in seen_patients:
                seen_patients.add(cin)
                
                # Déterminer le genre basé sur le prénom
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
    
    @patients_bp.route('/patients/<patient_id>', methods=['PUT'])   
    @token_required
    def update_patient(user_id, patient_id):
        try:
            db = current_app.config['db']
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'Données manquantes'}), 400
                
            # Vérifier que le patient appartient à l'utilisateur
            existing_image = db.images.find_one({
                '_id': ObjectId(patient_id),
                'utilisateurId': ObjectId(user_id)
            })
            
            if not existing_image:
                return jsonify({'error': 'Patient non trouvé'}), 404
                
            # Préparer les données à mettre à jour
            update_data = {}
            
            if 'name' in data:
                update_data['patient.nomComplet'] = data['name']
            if 'age' in data:
                update_data['patient.age'] = int(data['age'])
            if 'cin' in data:
                update_data['patient.cin'] = data['cin']
            if 'symptoms' in data:
                update_data['patient.symptomes'] = data['symptoms']
            if 'notes' in data:
                update_data['notes'] = data['notes']
                
            # Ajouter la date de modification
            update_data['dateModification'] = current_app.datetime.utcnow()
            
            # Mettre à jour le patient
            result = db.images.update_one(
                {'_id': ObjectId(patient_id), 'utilisateurId': ObjectId(user_id)},
                {'$set': update_data}
            )
            
            if result.modified_count == 0:
                return jsonify({'error': 'Aucune modification effectuée'}), 400
                
            return jsonify({
                'message': 'Patient mis à jour avec succès',
                'patient_id': patient_id
            }), 200
            
        except ValueError:
            return jsonify({'error': 'ID patient invalide'}), 400
        except Exception as e:
            current_app.logger.error(f'Erreur modification patient: {str(e)}')
            return jsonify({'error': 'Erreur lors de la modification du patient'}), 500


    @patients_bp.route('/patients/<patient_id>', methods=['DELETE'])
    @token_required
    def delete_patient(user_id, patient_id):
        try:
            db = current_app.config['db']
            
            # Vérifier que le patient appartient à l'utilisateur
            existing_image = db.images.find_one({
                '_id': ObjectId(patient_id),
                'utilisateurId': ObjectId(user_id)
            })
            
            if not existing_image:
                return jsonify({'error': 'Patient non trouvé'}), 404
                
            # Supprimer toutes les analyses associées
            db.analyses.delete_many({'imageId': ObjectId(patient_id)})
            
            # Supprimer tous les rapports associés
            db.rapports.delete_many({'analyseId': {'$in': [ObjectId(patient_id)]}})
            
            # Supprimer le patient (image)
            result = db.images.delete_one({
                '_id': ObjectId(patient_id),
                'utilisateurId': ObjectId(user_id)
            })
            
            if result.deleted_count == 0:
                return jsonify({'error': 'Patient non trouvé'}), 404
                
            # Supprimer le fichier physique si nécessaire
            try:
                import os
                filepath = existing_image.get('filepath')
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as file_error:
                current_app.logger.warning(f'Erreur suppression fichier: {str(file_error)}')
                
            return jsonify({
                'message': 'Patient supprimé avec succès',
                'patient_id': patient_id
            }), 200
            
        except ValueError:
            return jsonify({'error': 'ID patient invalide'}), 400
        except Exception as e:
            current_app.logger.error(f'Erreur suppression patient: {str(e)}')
            return jsonify({'error': 'Erreur lors de la suppression du patient'}), 500