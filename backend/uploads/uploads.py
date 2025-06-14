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
def upload_file(current_user):
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

    if file and allowed_file(file.filename):
        try:
            # Sauvegarder le fichier
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Enregistrement dans MongoDB
            db = current_app.config['db']
            result = db.images.insert_one({
                'filename': filename,
                'filepath': filepath,
                'upload_date': datetime.utcnow(),
                'user_id': ObjectId(current_user['_id']),
                'patient': {
                    'fullName': request.form['fullName'],
                    'age': int(request.form['age']),
                    'cin': request.form['cin'],
                    'symptoms': request.form['symptoms']
                },
                'notes': request.form.get('notes', ''),
                'status': 'pending',
                'metadata': {
                    'original_filename': file.filename,
                    'content_type': file.content_type
                }
            })

            return jsonify({
                'message': 'Fichier uploadé avec succès',
                'fileId': str(result.inserted_id),
                'filename': filename
            }), 200

        except Exception as e:
            current_app.logger.error(f'Erreur upload: {str(e)}')
            return jsonify({'error': 'Erreur lors du traitement du fichier'}), 500

    return jsonify({'error': 'Type de fichier non autorisé'}), 400