from flask import Blueprint, jsonify
from bson.objectid import ObjectId
from afficher_les_resultats.mongo_connection import get_db  # chemin corrigé si c'est dans le même dossier

results_bp = Blueprint('results', __name__)
db = get_db()
collection = db["analyse"]

@results_bp.route('/results/<string:analysis_id>', methods=['GET'])
def get_result(analysis_id):
    try:
        result = collection.find_one({"_id": ObjectId(analysis_id)})
        if result:
            result["_id"] = str(result["_id"])
            return jsonify(result), 200
        else:
            return jsonify({"message": "Analyse non trouvée"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
