# models/task.py - CRUD des tâches écologiques
# Chaque tâche est liée à un utilisateur et a une catégorie

import math
from database import get_db

# Les catégories et leurs estimations de CO2 économisé
# (valeurs approximatives, trouvées sur ademe.fr et différents sites)
CATEGORIES = {
    'Transport': '~2 kg CO2 economises',
    'Alimentation': '~1.5 kg CO2 economises',
    'Energie': '~1 kg CO2 economises',
    'Dechets': '~0.5 kg CO2 economises',
    'Eau': '~0.3 kg CO2 economises',
    'Numerique': '~0.8 kg CO2 economises',
    'Autre': 'Impact variable',
}


def creer_tache(titre, description, categorie, user_id):
    impact = CATEGORIES.get(categorie, 'Impact variable')
    conn = get_db()
    conn.execute(
        'INSERT INTO taches (titre, description, categorie, impact_co2, utilisateur_id) VALUES (?, ?, ?, ?, ?)',
        (titre, description, categorie, impact, user_id)
    )
    conn.commit()
    conn.close()


def get_taches(user_id, filtre=None, page=1, par_page=10):
    """
    Récupère les tâches paginées d'un utilisateur.
    filtre = None -> toutes, 'a_faire' -> pas cochées, 'accomplies' -> cochées
    """
    offset = (page - 1) * par_page
    conn = get_db()

    colonnes = 'id, titre, description, est_accomplie, categorie, impact_co2, date_creation'
    base_query = f'SELECT {colonnes} FROM taches WHERE utilisateur_id = ?'

    if filtre == 'a_faire':
        taches = conn.execute(
            base_query + ' AND est_accomplie = 0 ORDER BY date_creation DESC LIMIT ? OFFSET ?',
            (user_id, par_page, offset)
        ).fetchall()
    elif filtre == 'accomplies':
        taches = conn.execute(
            base_query + ' AND est_accomplie = 1 ORDER BY date_creation DESC LIMIT ? OFFSET ?',
            (user_id, par_page, offset)
        ).fetchall()
    else:
        # par défaut : les non-accomplies d'abord, puis les accomplies
        taches = conn.execute(
            base_query + ' ORDER BY est_accomplie ASC, date_creation DESC LIMIT ? OFFSET ?',
            (user_id, par_page, offset)
        ).fetchall()

    conn.close()
    return taches


def compter_taches(user_id, filtre=None):
    """Compte le nombre total de tâches pour la pagination."""
    conn = get_db()
    base = 'SELECT COUNT(*) as n FROM taches WHERE utilisateur_id = ?'

    if filtre == 'a_faire':
        n = conn.execute(base + ' AND est_accomplie = 0', (user_id,)).fetchone()['n']
    elif filtre == 'accomplies':
        n = conn.execute(base + ' AND est_accomplie = 1', (user_id,)).fetchone()['n']
    else:
        n = conn.execute(base, (user_id,)).fetchone()['n']

    conn.close()
    return n


def get_tache(tache_id):
    conn = get_db()
    tache = conn.execute(
        'SELECT id, titre, description, est_accomplie, categorie, impact_co2, utilisateur_id FROM taches WHERE id = ?',
        (tache_id,)
    ).fetchone()
    conn.close()
    return tache


def modifier_tache(tache_id, titre, description, categorie):
    impact = CATEGORIES.get(categorie, 'Impact variable')
    conn = get_db()
    conn.execute(
        'UPDATE taches SET titre = ?, description = ?, categorie = ?, impact_co2 = ? WHERE id = ?',
        (titre, description, categorie, impact, tache_id)
    )
    conn.commit()
    conn.close()


def basculer_statut(tache_id):
    """Inverse l'état accompli/non accompli. SQLite n'a pas de vrai booléen,
    on utilise 0/1 et NOT pour inverser."""
    conn = get_db()
    conn.execute('UPDATE taches SET est_accomplie = NOT est_accomplie WHERE id = ?', (tache_id,))
    conn.commit()
    conn.close()


def supprimer_tache(tache_id):
    conn = get_db()
    conn.execute('DELETE FROM taches WHERE id = ?', (tache_id,))
    conn.commit()
    conn.close()


def stats_utilisateur(user_id):
    """Retourne le nb total et accompli de tâches pour un utilisateur."""
    conn = get_db()
    total = conn.execute(
        'SELECT COUNT(*) as n FROM taches WHERE utilisateur_id = ?', (user_id,)
    ).fetchone()['n']
    accomplies = conn.execute(
        'SELECT COUNT(*) as n FROM taches WHERE utilisateur_id = ? AND est_accomplie = 1', (user_id,)
    ).fetchone()['n']
    conn.close()
    return {'total': total, 'accomplies': accomplies}


def stats_globales():
    """Stats pour le panel admin."""
    conn = get_db()
    total = conn.execute('SELECT COUNT(*) as n FROM taches').fetchone()['n']
    accomplies = conn.execute(
        'SELECT COUNT(*) as n FROM taches WHERE est_accomplie = 1'
    ).fetchone()['n']
    conn.close()
    return {'total': total, 'accomplies': accomplies}
