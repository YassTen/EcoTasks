# 🌱 EcoTasks

Application web de gestion de tâches éco-responsables, réalisée dans le cadre du cours **Numérique Durable (TI616)** — EFREI Paris.

## Concept

Un site sobre où les utilisateurs créent et suivent des actions écologiques au quotidien (prendre le vélo, réduire le plastique, éteindre les appareils en veille…).

## Stack technique

| Composant | Technologie | Pourquoi ? |
|---|---|---|
| Back-end | Python + Flask | Léger, rapide à développer, peu de dépendances |
| Base de données | SQLite | Pas de serveur à installer, un seul fichier |
| Front-end | HTML/CSS/JS vanilla | Pas de framework lourd, chargement instantané |
| Auth | bcrypt + sessions Flask | Hachage sécurisé, pas de JWT surdimensionné |

## Lancer le projet

```bash
# installer les dépendances
pip install -r requirements.txt

# lancer le serveur
python app.py
```

Le site est accessible sur **http://127.0.0.1:5000**

## Structure du projet

```
├── app.py              # Point d'entrée Flask
├── database.py         # Init et connexion SQLite
├── utils.py            # Décorateurs d'authentification
├── models/
│   ├── user.py         # CRUD utilisateurs + bcrypt
│   └── task.py         # CRUD tâches écologiques
├── routes/
│   ├── auth.py         # Inscription / Connexion / Déconnexion
│   ├── tasks.py        # Dashboard et gestion des tâches
│   ├── users.py        # Profil utilisateur
│   └── admin.py        # Panel admin
├── templates/          # Pages HTML (Jinja2)
├── static/
│   ├── style.css       # Feuille de style sobre
│   └── script.js       # JS minimal (~20 lignes)
└── requirements.txt    # Flask + bcrypt
```

## Engagements Green IT

- **Poids < 50 Ko par page** — pas d'images, polices système, pas de framework JS
- **Aucun tracker** — zéro cookie tiers, zéro analytics externe
- **SQLite** — pas de serveur de BDD supplémentaire
- **Pas de CDN** — tout est servi en local
- **HTML sémantique** — accessible et léger

## Équipe

Projet réalisé par l'équipe dans le cadre du module TI616, EFREI Paris 2025-2026.
