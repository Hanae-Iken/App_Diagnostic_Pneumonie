from flask import Blueprint, jsonify, current_app
from auth.utils import token_required
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from collections import defaultdict

dashboard_bp = Blueprint('dashboard_bp', __name__)

def calculer_total_analyses(db, user_id):
    """Calcule le nombre total d'analyses pour un utilisateur"""
    try:
        total = db.analyses.count_documents({'utilisateurId': ObjectId(user_id)})
        return total
    except Exception as e:
        print(f"Erreur calcul total analyses: {e}")
        return 0

def calculer_cas_pneumonie(db, user_id):
    """Calcule le nombre de cas de pneumonie détectés"""
    try:
        cas_pneumonie = db.analyses.count_documents({
            'utilisateurId': ObjectId(user_id),
            'resultat': 'pneumonie'
        })
        return cas_pneumonie
    except Exception as e:
        print(f"Erreur calcul cas pneumonie: {e}")
        return 0

def calculer_cas_normaux(db, user_id):
    """Calcule le nombre de cas normaux (sans pneumonie)"""
    try:
        cas_normaux = db.analyses.count_documents({
            'utilisateurId': ObjectId(user_id),
            'resultat': 'normal'
        })
        return cas_normaux
    except Exception as e:
        print(f"Erreur calcul cas normaux: {e}")
        return 0

def calculer_patients_suivis(db, user_id):
    """Calcule le nombre de patients uniques suivis"""
    try:
        # Utiliser aggregation pour compter les patients uniques par CIN
        pipeline = [
            {'$match': {'utilisateurId': ObjectId(user_id)}},
            {'$group': {'_id': '$patient.cin'}},
            {'$count': 'total_patients'}
        ]
        
        result = list(db.analyses.aggregate(pipeline))
        return result[0]['total_patients'] if result else 0
    except Exception as e:
        print(f"Erreur calcul patients suivis: {e}")
        return 0

def calculer_analyses_urgentes(db, user_id):
    """Calcule les analyses avec confiance faible (< 80%) ou résultats positifs récents"""
    try:
        # Analyses des dernières 24h avec pneumonie OU confiance < 0.8
        hier = datetime.utcnow() - timedelta(days=1)
        
        urgentes = db.analyses.count_documents({
            'utilisateurId': ObjectId(user_id),
            '$or': [
                {
                    'dateAnalyse': {'$gte': hier},
                    'resultat': 'pneumonie'
                },
                {
                    'confiance': {'$lt': 0.8}
                }
            ]
        })
        return urgentes
    except Exception as e:
        print(f"Erreur calcul analyses urgentes: {e}")
        return 0

def calculer_tendances(db, user_id):
    """Calcule les tendances par rapport à la période précédente"""
    try:
        # Comparer cette semaine vs semaine précédente
        maintenant = datetime.utcnow()
        debut_semaine = maintenant - timedelta(days=7)
        debut_semaine_precedente = maintenant - timedelta(days=14)
        
        # Cette semaine
        cette_semaine = db.analyses.count_documents({
            'utilisateurId': ObjectId(user_id),
            'dateAnalyse': {'$gte': debut_semaine}
        })
        
        # Semaine précédente
        semaine_precedente = db.analyses.count_documents({
            'utilisateurId': ObjectId(user_id),
            'dateAnalyse': {
                '$gte': debut_semaine_precedente,
                '$lt': debut_semaine
            }
        })
        
        # Calculer le pourcentage de changement
        if semaine_precedente == 0:
            changement = 100 if cette_semaine > 0 else 0
        else:
            changement = round(((cette_semaine - semaine_precedente) / semaine_precedente) * 100)
        
        return {
            'total_analyses': {
                'trend': 'up' if changement > 0 else 'down',
                'change': f'{abs(changement)}%'
            }
        }
    except Exception as e:
        print(f"Erreur calcul tendances: {e}")
        return {
            'total_analyses': {'trend': 'up', 'change': '0%'}
        }

def get_activites_recentes(db, user_id):
    """Récupère les 5 dernières activités"""
    try:
        pipeline = [
            {
                '$match': {'utilisateurId': ObjectId(user_id)}
            },
            {
                '$sort': {'dateAnalyse': -1}
            },
            {
                '$limit': 5
            },
            {
                '$project': {
                    'patient.nomComplet': 1,
                    'resultat': 1,
                    'confiance': 1,
                    'dateAnalyse': 1
                }
            }
        ]
        
        analyses = list(db.analyses.aggregate(pipeline))
        
        activites = []
        for analyse in analyses:
            # Calculer le temps écoulé
            temps_ecoule = datetime.utcnow() - analyse['dateAnalyse']
            if temps_ecoule.seconds < 3600:  # Moins d'1h
                temps_str = f"il y a {temps_ecoule.seconds // 60} minutes"
            elif temps_ecoule.seconds < 86400:  # Moins d'1 jour
                temps_str = f"il y a {temps_ecoule.seconds // 3600} heures"
            else:
                temps_str = f"il y a {temps_ecoule.days} jours"
            
            activites.append({
                'id': str(analyse['_id']),
                'patient': analyse['patient']['nomComplet'],
                'time': temps_str,
                'result': 'Positif' if analyse['resultat'] == 'pneumonie' else 'Négatif',
                'confidence': f"{round(analyse['confiance'] * 100)}%",
                'type': 'analysis'
            })
        
        return activites
    except Exception as e:
        print(f"Erreur activités récentes: {e}")
        return []

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats(user_id):
    """API principale pour récupérer toutes les statistiques du dashboard"""
    try:
        db = current_app.config["db"]
        
        # Calculer toutes les statistiques
        total_analyses = calculer_total_analyses(db, user_id)
        cas_pneumonie = calculer_cas_pneumonie(db, user_id)
        cas_normaux = calculer_cas_normaux(db, user_id)
        patients_suivis = calculer_patients_suivis(db, user_id)
        analyses_urgentes = calculer_analyses_urgentes(db, user_id)
        
        # Calculer les tendances
        tendances = calculer_tendances(db, user_id)
        
        # Activités récentes
        activites = get_activites_recentes(db, user_id)
        
        # Calculer les pourcentages pour l'aperçu santé
        if total_analyses > 0:
            precision = round((cas_normaux + cas_pneumonie) / total_analyses * 100)
            cas_resolus = round((cas_normaux + cas_pneumonie) / total_analyses * 100)
        else:
            precision = 0
            cas_resolus = 0
        
        # Préparer la réponse
        stats = {
            'stats': [
                {
                    'title': 'Total analyses',
                    'value': total_analyses,
                    'trend': tendances['total_analyses']['trend'],
                    'change': tendances['total_analyses']['change'],
                    'color': '#6366F1'
                },
                {
                    'title': 'Cas pneumonie',
                    'value': cas_pneumonie,
                    'trend': 'down',  # Toujours mieux quand ça baisse
                    'change': '5%',   # Valeur exemple
                    'color': '#EC4899'
                },
                {
                    'title': 'Patients suivis',
                    'value': patients_suivis,
                    'trend': 'up',
                    'change': '8%',
                    'color': '#10B981'
                },
                {
                    'title': 'Analyses urgentes',
                    'value': analyses_urgentes,
                    'trend': 'up',
                    'change': '23%',
                    'color': '#F59E0B'
                }
            ],
            'activities': activites,
            'health_stats': {
                'cas_resolus': cas_resolus,
                'precision': precision,
                'satisfaction': 92  # Valeur fixe pour l'exemple
            },
            'summary': {
                'total_analyses': total_analyses,
                'cas_pneumonie': cas_pneumonie,
                'cas_normaux': cas_normaux,
                'patients_suivis': patients_suivis
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"Erreur dashboard stats: {e}")
        current_app.logger.error(f'Erreur dashboard stats: {str(e)}')
        return jsonify({'error': 'Erreur lors du calcul des statistiques'}), 500

@dashboard_bp.route('/api/dashboard/calendar', methods=['GET'])
@token_required
def get_calendar_data(user_id):
    """API pour récupérer les données du calendrier dynamique"""
    try:
        # Date actuelle
        maintenant = datetime.now()
        
        # Calculer les jours du mois courant
        premier_jour = maintenant.replace(day=1)
        
        # Jours de la semaine précédente si nécessaire
        jours_precedents = []
        if premier_jour.weekday() > 0:  # Si le 1er n'est pas un lundi
            for i in range(premier_jour.weekday()):
                jour_precedent = premier_jour - timedelta(days=premier_jour.weekday() - i)
                jours_precedents.append(jour_precedent.day)
        
        # Jours du mois courant
        import calendar
        _, nb_jours = calendar.monthrange(maintenant.year, maintenant.month)
        jours_mois = list(range(1, nb_jours + 1))
        
        # Tous les jours à afficher
        tous_jours = jours_precedents + jours_mois
        
        # Nom du mois en français
        mois_fr = [
            'JANVIER', 'FÉVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN',
            'JUILLET', 'AOÛT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE', 'DÉCEMBRE'
        ]
        
        return jsonify({
            'current_day': maintenant.day,
            'current_month': mois_fr[maintenant.month - 1],
            'current_year': maintenant.year,
            'days': tous_jours,
            'days_in_current_month': nb_jours
        }), 200
        
    except Exception as e:
        print(f"Erreur calendrier: {e}")
        return jsonify({'error': 'Erreur lors de la génération du calendrier'}), 500