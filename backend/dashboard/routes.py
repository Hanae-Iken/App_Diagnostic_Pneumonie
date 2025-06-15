from flask import Blueprint, jsonify, current_app
from datetime import datetime, timedelta
from pymongo import DESCENDING
from bson import ObjectId
import json

# Créer le blueprint pour les routes du dashboard
dashboard_bp = Blueprint('dashboard', __name__)

def serialize_objectid(obj):
    """Convertit les ObjectId en string pour la sérialisation JSON"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: serialize_objectid(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_objectid(item) for item in obj]
    else:
        return obj

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Récupère les statistiques du dashboard"""
    try:
        db = current_app.config["db"]
        
        # Statistiques générales
        total_analyses = db.analyses.count_documents({})
        total_images = db.images.count_documents({})
        
        # Cas de pneumonie (analyses avec résultat positif)
        cas_pneumonie = db.analyses.count_documents({
            'resultats.resultat': {'$in': ['Pneumonie', 'Positif', 'pneumonie', 'positif']}
        })
        
        # Patients uniques suivis
        patients_suivis = len(db.analyses.distinct('patient.cin'))
        
        # Analyses récentes (dernières 24h) considérées comme urgentes
        date_limite = datetime.utcnow() - timedelta(hours=24)
        analyses_urgentes = db.analyses.count_documents({
            'dateAnalyse': {'$gte': date_limite},
            'priorite': {'$in': ['haute', 'urgente']}
        })
        
        # Si pas d'analyses avec priorité, compter les analyses récentes
        if analyses_urgentes == 0:
            analyses_urgentes = db.analyses.count_documents({
                'dateAnalyse': {'$gte': date_limite}
            })
        
        # Calcul des tendances (comparaison avec la période précédente)
        date_limite_precedente = datetime.utcnow() - timedelta(days=7)
        
        # Analyses de cette semaine vs semaine précédente
        analyses_cette_semaine = db.analyses.count_documents({
            'dateAnalyse': {'$gte': date_limite_precedente}
        })
        analyses_semaine_precedente = db.analyses.count_documents({
            'dateAnalyse': {
                '$gte': datetime.utcnow() - timedelta(days=14),
                '$lt': date_limite_precedente
            }
        })
        
        # Calcul du pourcentage de changement
        def calculer_tendance(actuel, precedent):
            if precedent == 0:
                return 100 if actuel > 0 else 0
            return round(((actuel - precedent) / precedent) * 100)
        
        tendance_analyses = calculer_tendance(analyses_cette_semaine, analyses_semaine_precedente)
        
        # Cas pneumonie cette semaine vs précédente
        pneumonie_cette_semaine = db.analyses.count_documents({
            'dateAnalyse': {'$gte': date_limite_precedente},
            'resultats.resultat': {'$in': ['Pneumonie', 'Positif', 'pneumonie', 'positif']}
        })
        pneumonie_semaine_precedente = db.analyses.count_documents({
            'dateAnalyse': {
                '$gte': datetime.utcnow() - timedelta(days=14),
                '$lt': date_limite_precedente
            },
            'resultats.resultat': {'$in': ['Pneumonie', 'Positif', 'pneumonie', 'positif']}
        })
        
        tendance_pneumonie = calculer_tendance(pneumonie_cette_semaine, pneumonie_semaine_precedente)
        
        return jsonify({
            'success': True,
            'data': {
                'totalAnalyses': {
                    'value': total_analyses,
                    'change': abs(tendance_analyses),
                    'trend': 'up' if tendance_analyses >= 0 else 'down'
                },
                'casPneumonie': {
                    'value': cas_pneumonie,
                    'change': abs(tendance_pneumonie),
                    'trend': 'down' if tendance_pneumonie <= 0 else 'up'  # Down est bon pour pneumonie
                },
                'patientsSuivis': {
                    'value': patients_suivis,
                    'change': 8,  # Pourcentage fixe ou calculé selon vos besoins
                    'trend': 'up'
                },
                'analysesUrgentes': {
                    'value': analyses_urgentes,
                    'change': 23,
                    'trend': 'up'
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/dashboard/activities', methods=['GET'])
def get_recent_activities():
    """Récupère les activités récentes"""
    try:
        db = current_app.config["db"]
        
        activities = []
        
        # Récupérer les analyses récentes
        recent_analyses = db.analyses.find().sort('dateAnalyse', DESCENDING).limit(10)
        
        for analyse in recent_analyses:
            # Calculer le temps écoulé
            if 'dateAnalyse' in analyse:
                time_diff = datetime.utcnow() - analyse['dateAnalyse']
                if time_diff.days > 0:
                    time_str = f"il y a {time_diff.days} jour{'s' if time_diff.days > 1 else ''}"
                elif time_diff.seconds > 3600:
                    hours = time_diff.seconds // 3600
                    time_str = f"il y a {hours} heure{'s' if hours > 1 else ''}"
                else:
                    minutes = time_diff.seconds // 60
                    time_str = f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
            else:
                time_str = "récemment"
            
            # Extraire les informations du patient
            patient_nom = "Patient"
            if 'patient' in analyse:
                if 'nom' in analyse['patient'] and 'prenom' in analyse['patient']:
                    patient_nom = f"{analyse['patient']['prenom']} {analyse['patient']['nom']}"
                elif 'nom' in analyse['patient']:
                    patient_nom = analyse['patient']['nom']
            
            # Extraire le résultat et la confiance
            resultat = "En cours"
            confiance = 0
            if 'resultats' in analyse:
                if 'resultat' in analyse['resultats']:
                    resultat = analyse['resultats']['resultat']
                if 'confiance' in analyse['resultats']:
                    confiance = int(analyse['resultats']['confiance'] * 100) if analyse['resultats']['confiance'] <= 1 else int(analyse['resultats']['confiance'])
            
            activities.append({
                'id': str(analyse['_id']),
                'patient': patient_nom,
                'time': time_str,
                'result': 'Négatif' if resultat.lower() in ['normal', 'negatif', 'négatif'] else 'Positif',
                'confidence': f"{confiance}%",
                'type': 'analysis'
            })
        
        # Récupérer les nouveaux patients (basé sur les images récentes avec nouveaux patients)
        recent_images = db.images.find({
            'dateUpload': {'$gte': datetime.utcnow() - timedelta(days=7)}
        }).sort('dateUpload', DESCENDING).limit(5)
        
        seen_patients = set()
        for image in recent_images:
            if 'patient' in image and 'cin' in image['patient']:
                patient_cin = image['patient']['cin']
                if patient_cin not in seen_patients:
                    seen_patients.add(patient_cin)
                    
                    # Vérifier si c'est vraiment un nouveau patient
                    patient_analyses_count = db.analyses.count_documents({
                        'patient.cin': patient_cin
                    })
                    
                    if patient_analyses_count <= 1:  # Nouveau patient
                        time_diff = datetime.utcnow() - image['dateUpload']
                        if time_diff.days > 0:
                            time_str = f"il y a {time_diff.days} jour{'s' if time_diff.days > 1 else ''}"
                        elif time_diff.seconds > 3600:
                            hours = time_diff.seconds // 3600
                            time_str = f"il y a {hours} heure{'s' if hours > 1 else ''}"
                        else:
                            minutes = time_diff.seconds // 60
                            time_str = f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
                        
                        patient_nom = "Nouveau Patient"
                        if 'nom' in image['patient'] and 'prenom' in image['patient']:
                            patient_nom = f"{image['patient']['prenom']} {image['patient']['nom']}"
                        
                        activities.append({
                            'id': str(image['_id']),
                            'patient': patient_nom,
                            'time': time_str,
                            'action': 'Nouveau patient',
                            'type': 'new'
                        })
        
        # Trier toutes les activités par date (plus récent en premier)
        activities.sort(key=lambda x: x['time'], reverse=False)
        
        return jsonify({
            'success': True,
            'data': activities[:8]  # Limiter à 8 activités
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/dashboard/health-overview', methods=['GET'])
def get_health_overview():
    """Récupère l'aperçu santé avec des statistiques de performance"""
    try:
        db = current_app.config["db"]
        
        # Cas résolus (analyses terminées)
        total_analyses = db.analyses.count_documents({})
        analyses_terminees = db.analyses.count_documents({
            'statut': {'$in': ['termine', 'completed', 'fini']}
        })
        
        # Si pas de statut spécifique, considérer toutes les analyses avec résultats comme résolues
        if analyses_terminees == 0:
            analyses_terminees = db.analyses.count_documents({
                'resultats.resultat': {'$exists': True, '$ne': ''}
            })
        
        pourcentage_resolus = int((analyses_terminees / total_analyses * 100)) if total_analyses > 0 else 0
        
        # Précision moyenne (basée sur la confiance des résultats)
        pipeline_precision = [
            {
                '$match': {
                    'resultats.confiance': {'$exists': True}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'precision_moyenne': {'$avg': '$resultats.confiance'}
                }
            }
        ]
        
        precision_result = list(db.analyses.aggregate(pipeline_precision))
        precision_moyenne = 85  # Valeur par défaut
        
        if precision_result:
            precision_val = precision_result[0]['precision_moyenne']
            # Si la confiance est entre 0 et 1, multiplier par 100
            if precision_val <= 1:
                precision_moyenne = int(precision_val * 100)
            else:
                precision_moyenne = int(precision_val)
        
        # Satisfaction (simulée basée sur les résultats corrects vs incorrects)
        # Pour une vraie application, cela viendrait des feedbacks utilisateurs
        satisfaction = min(95, max(85, precision_moyenne + 5))  # Entre 85% et 95%
        
        return jsonify({
            'success': True,
            'data': {
                'casResolus': pourcentage_resolus,
                'precision': precision_moyenne,
                'satisfaction': satisfaction
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/dashboard/tasks', methods=['GET'])
def get_upcoming_tasks():
    """Récupère les tâches à venir basées sur les analyses en cours et les priorités"""
    try:
        db = current_app.config["db"]
        
        tasks = []
        
        # Analyses en attente de validation
        analyses_en_attente = db.analyses.count_documents({
            'statut': {'$in': ['en_cours', 'pending', 'attente']}
        })
        
        if analyses_en_attente > 0:
            tasks.append({
                'id': 1,
                'title': f'Valider {analyses_en_attente} analyse{"s" if analyses_en_attente > 1 else ""}',
                'time': '10:00 AM',
                'priority': 'high'
            })
        
        # Cas critiques (pneumonie détectée)
        cas_critiques = db.analyses.count_documents({
            'resultats.resultat': {'$in': ['Pneumonie', 'Positif', 'pneumonie', 'positif']},
            'dateAnalyse': {'$gte': datetime.utcnow() - timedelta(days=1)}
        })
        
        if cas_critiques > 0:
            tasks.append({
                'id': 2,
                'title': f'Revue de {cas_critiques} cas critique{"s" if cas_critiques > 1 else ""}',
                'time': '14:30 PM',
                'priority': 'high'
            })
        
        # Images en attente d'analyse
        images_en_attente = db.images.count_documents({
            'pret_pour_analyse': True,
            'analyseId': {'$exists': False}
        })
        
        if images_en_attente > 0:
            tasks.append({
                'id': 3,
                'title': f'Analyser {images_en_attente} image{"s" if images_en_attente > 1 else ""} en attente',
                'time': 'Aujourd\'hui',
                'priority': 'medium'
            })
        
        # Tâche de maintenance système (exemple)
        tasks.append({
            'id': 4,
            'title': 'Sauvegarde quotidienne',
            'time': 'Demain',
            'priority': 'low'
        })
        
        return jsonify({
            'success': True,
            'data': tasks[:5]  # Limiter à 5 tâches
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500