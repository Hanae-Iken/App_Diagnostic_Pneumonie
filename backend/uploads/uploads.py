import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
from auth.utils import token_required

upload_bp = Blueprint("upload_bp", __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
@token_required
def upload_file(user_id):
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        db = current_app.config["db"]
        db.images.insert_one({
            "nomFichier": filename,
            "dateTeleversement": datetime.utcnow(),
            "utilisateurId": ObjectId(user_id)
        })

        return jsonify({
            "message": "Image téléversée avec succès ✅",
            "fichier": filename
        })

    return jsonify({"error": "Extension non autorisée"}), 400
