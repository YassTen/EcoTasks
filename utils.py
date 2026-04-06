# Décorateurs pour protéger les routes
# On s'inspire de la doc Flask mais adapté à nos besoins

from functools import wraps
from flask import session, redirect, url_for, flash


def login_requis(f):
    """Redirige vers /connexion si l'utilisateur n'est pas connecté."""
    @wraps(f)  # wraps garde le nom original de la fonction, sinon Flask plante
    def wrapper(*args, **kwargs):
        if 'utilisateur_id' not in session:
            flash('Connectez-vous d\'abord.', 'erreur')
            return redirect(url_for('auth.connexion'))
        return f(*args, **kwargs)
    return wrapper


def admin_requis(f):
    """Pareil que login_requis mais vérifie aussi que c'est un admin."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'utilisateur_id' not in session:
            return redirect(url_for('auth.connexion'))
        if session.get('role') != 'admin':
            flash('Accès réservé aux administrateurs.', 'erreur')
            return redirect(url_for('taches.tableau_de_bord'))
        return f(*args, **kwargs)
    return wrapper
