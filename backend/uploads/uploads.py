from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
import os
from auth.utils import token_required

upload_bp = Blueprint('upload_bp', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm'}

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(user_id):  # Le décorateur token_required passe user_id
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
            return jsonify({'error': 'Type de fichier non autorisé. Utilisez: png, jpg, jpeg, dcm'}), 400

        # Sauvegarder le fichier
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Enregistrement dans MongoDB
        db = current_app.config['db']
        
        # Structure adaptée aux champs du frontend
        image_data = {
            'filename': filename,
            'filepath': filepath,
            'dateUpload': datetime.utcnow(),
            'utilisateurId': ObjectId(user_id),  # Utilisateur qui a uploadé
            'patient': {
                'nomComplet': request.form['fullName'],
                'age': int(request.form['age']),
                'cin': request.form['cin'],
                'symptomes': request.form['symptoms']
            },
            'notes': request.form.get('notes', ''),
            'statut': 'en_attente',  # en_attente, analyse, termine
            'metadata': {
                'nomOriginal': file.filename,
                'typeContenu': file.content_type,
                'taille': os.path.getsize(filepath)
            }
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
            }
        }), 200

    except ValueError as e:
        return jsonify({'error': 'Âge invalide - doit être un nombre'}), 400
    except Exception as e:
        current_app.logger.error(f'Erreur upload: {str(e)}')
        return jsonify({'error': 'Erreur lors du traitement du fichier'}), 500