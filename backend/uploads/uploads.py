# from flask import Blueprint, request, jsonify, current_app
# from werkzeug.utils import secure_filename
# from bson import ObjectId
# from datetime import datetime
# import os
# from auth.utils import token_required

# upload_bp = Blueprint('upload_bp', __name__)
# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm', 'dicom'}

# # Créer le dossier uploads s'il n'existe pas
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @upload_bp.route('/upload', methods=['POST'])
# @token_required
# def upload_file(user_id):
#     try:
#         # Vérifier que tous les champs requis sont présents
#         required_fields = ['fullName', 'age', 'cin', 'symptoms']
#         for field in required_fields:
#             if field not in request.form:
#                 return jsonify({'error': f'Le champ {field} est requis'}), 400

#         # Vérifier le fichier
#         if 'file' not in request.files:
#             return jsonify({'error': 'Aucun fichier envoyé'}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'Aucun fichier sélectionné'}), 400

#         if not file or not allowed_file(file.filename):
#             return jsonify({'error': 'Type de fichier non autorisé. Utilisez: png, jpg, jpeg, dcm, dicom'}), 400

#         # Sauvegarder le fichier
#         filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)

#         # Enregistrement dans MongoDB
#         db = current_app.config['db']
        
#         # Structure adaptée pour l'analyse IA
#         image_data = {
#             'filename': filename,
#             'filepath': filepath,
#             'dateUpload': datetime.utcnow(),
#             'utilisateurId': ObjectId(user_id),
#             'patient': {
#                 'nomComplet': request.form['fullName'],
#                 'age': int(request.form['age']),
#                 'cin': request.form['cin'],
#                 'symptomes': request.form['symptoms']
#             },
#             'notes': request.form.get('notes', ''),
#             'statut': 'en_attente',  # en_attente -> analyse -> termine
#             'metadata': {
#                 'nomOriginal': file.filename,
#                 'typeContenu': file.content_type,
#                 'taille': os.path.getsize(filepath)
#             },
#             # Champs pour l'IA
#             'pret_pour_analyse': True,
#             'type_examen': request.form.get('examType', 'radiographie')  # par défaut
#         }

#         result = db.images.insert_one(image_data)

#         return jsonify({
#             'message': 'Fichier uploadé avec succès',
#             'fileId': str(result.inserted_id),
#             'filename': filename,
#             'patient': {
#                 'nomComplet': request.form['fullName'],
#                 'age': request.form['age'],
#                 'cin': request.form['cin']
#             },
#             'status': 'pret_pour_analyse'
#         }), 200

#     except ValueError as e:
#         return jsonify({'error': 'Âge invalide - doit être un nombre'}), 400
#     except Exception as e:
#         current_app.logger.error(f'Erreur upload: {str(e)}')
#         return jsonify({'error': 'Erreur lors du traitement du fichier'}), 500

# @upload_bp.route('/api/images/<user_id>', methods=['GET'])
# @token_required
# def get_user_images(current_user_id, user_id):
#     """
#     Récupère les images d'un utilisateur pour l'analyse
#     """
#     try:
#         db = current_app.config['db']
        
#         # Vérifier que l'utilisateur accède à ses propres images ou est admin
#         if current_user_id != user_id:
#             user = db.users.find_one({'_id': ObjectId(current_user_id)})
#             if not user or user.get('role') != 'admin':
#                 return jsonify({'error': 'Accès non autorisé'}), 403
        
#         # Récupérer les images
#         images = list(db.images.find(
#             {'utilisateurId': ObjectId(user_id)},
#             {'filepath': 0}  # Ne pas exposer le chemin complet
#         ).sort('dateUpload', -1))
        
#         # Convertir ObjectId en string
#         for img in images:
#             img['_id'] = str(img['_id'])
#             img['utilisateurId'] = str(img['utilisateurId'])
            
#         return jsonify({
#             'images': images,
#             'count': len(images)
#         }), 200
        
#     except Exception as e:
#         current_app.logger.error(f'Erreur récupération images: {str(e)}')
#         return jsonify({'error': 'Erreur lors de la récupération'}), 500


from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
import os
from auth.utils import token_required

upload_bp = Blueprint('upload_bp', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm', 'dicom'}

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(user_id):
    try:
        # Vérifier que tous les champs requis sont présents
        required_fields = ['fullName', 'age', 'cin', 'symptoms']
        for field in required_fields:
            if field not in request.form:
                return jsonify({'error': f'Le champ {field} est requis'}), 400

        # Vérifier le fichier
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier envoyé'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400

        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé. Utilisez: png, jpg, jpeg, dcm, dicom'}), 400

        # Sauvegarder le fichier
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Enregistrement dans MongoDB
        db = current_app.config['db']
        
        # Structure adaptée pour l'analyse IA
        image_data = {
            'filename': filename,
            'filepath': filepath,
            'dateUpload': datetime.utcnow(),
            'utilisateurId': ObjectId(user_id),
            'patient': {
                'nomComplet': request.form['fullName'],
                'age': int(request.form['age']),
                'cin': request.form['cin'],
                'symptomes': request.form['symptoms']
            },
            'notes': request.form.get('notes', ''),
            'statut': 'en_attente',  # en_attente -> analyse -> termine
            'metadata': {
                'nomOriginal': file.filename,
                'typeContenu': file.content_type,
                'taille': os.path.getsize(filepath)
            },
            # Champs pour l'IA
            'pret_pour_analyse': True,
            'type_examen': request.form.get('examType', 'radiographie')  # par défaut
        }

        result = db.images.insert_one(image_data)

        return jsonify({
            'message': 'Fichier uploadé avec succès',
            'fileId': str(result.inserted_id),
            'filename': filename,
            'patient': {
                'nomComplet': request.form['fullName'],
                'age': request.form['age'],
                'cin': request.form['cin']
            },
            'status': 'pret_pour_analyse'
        }), 200

    except ValueError as e:
        return jsonify({'error': 'Âge invalide - doit être un nombre'}), 400
    except Exception as e:
        current_app.logger.error(f'Erreur upload: {str(e)}')
        return jsonify({'error': 'Erreur lors du traitement du fichier'}), 500