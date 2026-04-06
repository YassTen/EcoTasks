# models/task.py - CRUD des tâches écologiques
# Chaque tâche est liée à un utilisateur et a une catégorie

from database import get_db

# Les catégories et leurs estimations de CO2 économisé
# (valeurs approximatives, trouvées sur ademe.fr et différents sites)
CATEGORIES = {
    'Transport': '~2 kg CO₂ économisés',
    'Alimentation': '~1.5 kg CO₂ économisés',
    'Énergie': '~1 kg CO₂ économisés',
    'Déchets': '~0.5 kg CO₂ économisés',
    'Eau': '~0.3 kg CO₂ économisés',
    'Numérique': '~0.8 kg CO₂ économisés',
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


def get_taches(user_id, filtre=None):
    """
    Récupère les tâches d'un utilisateur.
    filtre = None -> toutes, 'a_faire' -> pas cochées, 'accomplies' -> cochées
    """
    conn = get_db()

    base_query = 'SELECT * FROM taches WHERE utilisateur_id = ?'

    if filtre == 'a_faire':
        taches = conn.execute(
            base_query + ' AND est_accomplie = 0 ORDER BY date_creation DESC', (user_id,)
        ).fetchall()
    elif filtre == 'accomplies':
        taches = conn.execute(
            base_query + ' AND est_accomplie = 1 ORDER BY date_creation DESC', (user_id,)
        ).fetchall()
    else:
        # par défaut : les non-accomplies d'abord, puis les accomplies
        taches = conn.execute(
            base_query + ' ORDER BY est_accomplie ASC, date_creation DESC', (user_id,)
        ).fetchall()

    conn.close()
    return taches


def get_tache(tache_id):
    conn = get_db()
    tache = conn.execute('SELECT * FROM taches WHERE id = ?', (tache_id,)).fetchone()
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
