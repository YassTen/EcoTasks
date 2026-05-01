-- init_db.sql - Script de creation des tables EcoTasks
-- Base de donnees : SQLite
-- Ce script peut etre execute pour initialiser la base manuellement :
--   sqlite3 ecotasks.db < database/init_db.sql

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role TEXT DEFAULT 'utilisateur',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table des taches ecologiques (entite metier)
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
);

-- Index pour optimiser les requetes frequentes (Green IT : moins de CPU)
CREATE INDEX IF NOT EXISTS idx_taches_utilisateur ON taches(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_email ON utilisateurs(email);
