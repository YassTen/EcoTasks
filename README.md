# EcoTasks

Application web de gestion de taches eco-responsables, realisee dans le cadre du cours **Numerique Durable (TI616)** — EFREI Paris.

## Site deploye

**URL : [A COMPLETER APRES DEPLOIEMENT RENDER]**

## Concept

Un site sobre ou les utilisateurs creent et suivent des actions ecologiques au quotidien (prendre le velo, reduire le plastique, eteindre les appareils en veille…).

## Equipe

| Membre | Role |
|---|---|
| Yassine Tenzekhti | Developpement back-end, authentification, deploiement |
| [A COMPLETER] | [Role] |
| [A COMPLETER] | [Role] |
| [A COMPLETER] | [Role] |

Coordinateur du module : Yvan GUIFO

## Stack technique

| Composant | Technologie | Justification Green IT |
|---|---|---|
| Back-end | Python + Flask | Leger, rapide, 3 dependances seulement |
| Base de donnees | SQLite | Pas de serveur a installer, un seul fichier |
| Front-end | HTML/CSS/JS vanilla | Pas de framework lourd, chargement instantane |
| Auth | bcrypt + sessions Flask | Hachage securise, pas de JWT surdimensionne |
| Deploiement | Render (gunicorn) | Tier gratuit, auto-deploy depuis GitHub |

## Lancer le projet en local

```bash
# cloner le depot
git clone https://github.com/YassTen/EcoTasks.git
cd EcoTasks

# installer les dependances
pip install -r requirements.txt

# lancer le serveur
python app.py
```

Le site est accessible sur **http://127.0.0.1:5000**

## Structure du projet

```
├── app.py                  # Point d'entree Flask
├── database.py             # Init et connexion SQLite
├── utils.py                # Decorateurs d'authentification
├── render.yaml             # Config deploiement Render
├── models/
│   ├── user.py             # CRUD utilisateurs + bcrypt
│   └── task.py             # CRUD taches ecologiques
├── routes/
│   ├── auth.py             # Inscription / Connexion / Deconnexion
│   ├── tasks.py            # Dashboard et gestion des taches
│   ├── users.py            # Profil utilisateur
│   └── admin.py            # Panel admin
├── templates/              # Pages HTML (Jinja2)
├── static/
│   ├── style.css           # Feuille de style sobre + mode sombre
│   └── script.js           # JS minimal (~20 lignes)
├── database/
│   └── init_db.sql         # Script SQL d'initialisation
├── docs/                   # Rapport PDF, diagrammes UML, wireframes
├── .env.example            # Variables d'environnement (modele)
├── requirements.txt        # flask + bcrypt + gunicorn
└── README.md
```

## Conventions de commit

```
feat: nouvelle fonctionnalite
fix: correction de bug
style: changement CSS/UI sans impact fonctionnel
docs: modification de documentation
refactor: reorganisation de code sans changement fonctionnel
```

## Engagements Green IT

- **Poids < 50 Ko par page** — pas d'images, polices systeme, pas de framework JS
- **Aucun tracker** — zero cookie tiers, zero analytics externe
- **SQLite** — pas de serveur de BDD supplementaire
- **Pas de CDN** — tout est servi en local
- **Mode sombre** — automatique selon les preferences systeme (economies OLED)
- **HTML semantique** — accessible et leger
- **3 dependances Python** — flask, bcrypt, gunicorn

## Rapport

Le rapport PDF est disponible dans le dossier [`/docs`](docs/).
