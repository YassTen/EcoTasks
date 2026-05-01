# database.py - Connexion et init SQLite
# On part sur SQLite plutôt que MySQL/PostgreSQL parce que pour un projet
# local avec quelques utilisateurs, ça suffit largement et ça évite d'installer un serveur de BDD en plus (sobriété numérique)

import sqlite3
import os

CHEMIN_BD = os.path.join(os.path.dirname(__file__), 'ecotasks.db')


def get_db():
    conn = sqlite3.connect(CHEMIN_BD)
    conn.row_factory = sqlite3.Row  # permet d'accéder aux colonnes par nom plutôt que par index
    # Piège classique SQLite : les foreign keys sont désactivées par défaut !
    # Sans cette ligne, ON DELETE CASCADE ne marche pas du tout
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Crée les tables et index au premier lancement. Si elles existent déjà, ne fait rien."""
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role TEXT DEFAULT 'utilisateur',
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS taches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT DEFAULT '',
            est_accomplie INTEGER DEFAULT 0,
            categorie TEXT DEFAULT 'Autre',
            impact_co2 TEXT DEFAULT '',
            utilisateur_id INTEGER NOT NULL,
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
        )
    ''')

    # Index sur les colonnes fréquemment interrogées (Green IT : requêtes plus rapides = moins de CPU)
    c.execute('CREATE INDEX IF NOT EXISTS idx_taches_utilisateur ON taches(utilisateur_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_utilisateurs_email ON utilisateurs(email)')

    conn.commit()
    conn.close()
