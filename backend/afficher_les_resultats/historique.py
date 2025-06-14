from flask import Blueprint, jsonify, current_app
from auth.utils import token_required
from bson.objectid import ObjectId

history_bp = Blueprint('history_bp', __name__)  # Change le nom si nécessaire

@history_bp.route('/history', methods=['GET'])
@token_required
def get_history(user_id):
    db = current_app.config["db"]

    historiques = list(db.analyses.find(
        {"user_id": ObjectId(user_id)},
        {"_id": 0}  # exclure le champ _id
    ))

    return jsonify(historiques), 200
