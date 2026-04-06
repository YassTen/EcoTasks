# app.py - Point d'entrée de l'application EcoTasks
# Flask + SQLite, pas besoin de plus pour un projet local

import os
from flask import Flask, render_template
from database import init_db
from routes.auth import auth_bp
from routes.tasks import taches_bp
from routes.users import utilisateurs_bp
from routes.admin import admin_bp

app = Flask(__name__)

# Clé secrète pour signer les cookies de session
# En prod il faudrait une vraie clé aléatoire dans une variable d'env,
# mais pour du local ça suffit
app.secret_key = os.environ.get('CLE_SECRETE', 'ecotasks-dev-2025-clé-temporaire')

# Enregistrement des blueprints (un par "module" de l'app)
app.register_blueprint(auth_bp)
app.register_blueprint(taches_bp)
app.register_blueprint(utilisateurs_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def accueil():
    return render_template('index.html')


@app.errorhandler(404)
def page_404(e):
    return render_template('erreur.html', code=404, message='Page introuvable'), 404


@app.errorhandler(500)
def page_500(e):
    return render_template('erreur.html', code=500, message='Erreur serveur'), 500


if __name__ == '__main__':
    init_db()  # crée les tables au premier lancement
    app.run(debug=True, host='127.0.0.1', port=5000)
