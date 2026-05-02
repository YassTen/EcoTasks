# app.py - Point d'entree de l'application EcoTasks
# Flask + SQLite, pas besoin de plus pour un projet local

import os
from flask import Flask, render_template
from database import init_db
from routes.auth import auth_bp
from routes.tasks import taches_bp
from routes.users import utilisateurs_bp
from routes.admin import admin_bp

app = Flask(__name__)

# Cle secrete pour signer les cookies de session
# En prod il faudrait une vraie cle aleatoire dans une variable d'env
app.secret_key = os.environ.get('CLE_SECRETE', 'ecotasks-dev-2025-cle-temporaire')

# Enregistrement des blueprints (un par "module" de l'app)
app.register_blueprint(auth_bp)
app.register_blueprint(taches_bp)
app.register_blueprint(utilisateurs_bp)
app.register_blueprint(admin_bp)

# Init de la base au demarrage, que ce soit avec gunicorn ou en local
# gunicorn importe app sans passer par if __name__ == '__main__',
# donc init_db() doit etre ici pour que les tables existent en prod
init_db()


@app.route('/')
def accueil():
    return render_template('index.html')


@app.errorhandler(403)
def page_403(e):
    return render_template('erreur.html', code=403, message='Acces interdit'), 403


@app.errorhandler(404)
def page_404(e):
    return render_template('erreur.html', code=404, message='Page introuvable'), 404


@app.errorhandler(500)
def page_500(e):
    return render_template('erreur.html', code=500, message='Erreur serveur'), 500


if __name__ == '__main__':
    # en local seulement : mode debug + affichage de l'IP reseau
    import socket

    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    local_ip = get_local_ip()
    print("\n" + "=" * 60)
    print("L'application est accessible sur votre reseau local !")
    print(f"Lien a partager : http://{local_ip}:5000")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
