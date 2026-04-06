# routes/users.py - Profil utilisateur : affichage, modif, suppression

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import get_user, modifier_utilisateur, changer_mot_de_passe, supprimer_utilisateur, get_user_par_email
from models.task import stats_utilisateur
from utils import login_requis

utilisateurs_bp = Blueprint('utilisateurs', __name__)


@utilisateurs_bp.route('/profil')
@login_requis
def profil():
    user = get_user(session['utilisateur_id'])
    if not user:
        # cas improbable mais au cas où le compte a été supprimé par un admin
        session.clear()
        return redirect(url_for('auth.connexion'))

    stats = stats_utilisateur(session['utilisateur_id'])
    return render_template('profil.html', utilisateur=user, stats=stats)


@utilisateurs_bp.route('/profil/modifier', methods=['GET', 'POST'])
@login_requis
def modifier_profil():
    user = get_user(session['utilisateur_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.connexion'))

    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip().lower()
        nouveau_mdp = request.form.get('nouveau_mdp', '')
        confirm_mdp = request.form.get('confirmation_mdp', '')

        if not nom or not email:
            flash('Le nom et l\'email sont obligatoires.', 'erreur')
            return render_template('modifier_profil.html', utilisateur=user)

        # vérif qu'un autre utilisateur n'a pas déjà cet email
        autre = get_user_par_email(email)
        if autre and autre['id'] != session['utilisateur_id']:
            flash('Cet email est déjà utilisé.', 'erreur')
            return render_template('modifier_profil.html', utilisateur=user)

        if not modifier_utilisateur(session['utilisateur_id'], nom, email):
            flash('Erreur lors de la modification.', 'erreur')
            return render_template('modifier_profil.html', utilisateur=user)

        # changement de mdp seulement si le champ est rempli
        if nouveau_mdp:
            if len(nouveau_mdp) < 6:
                flash('Le mot de passe doit faire au moins 6 caractères.', 'erreur')
                return render_template('modifier_profil.html', utilisateur=user)
            if nouveau_mdp != confirm_mdp:
                flash('Les mots de passe ne correspondent pas.', 'erreur')
                return render_template('modifier_profil.html', utilisateur=user)
            changer_mot_de_passe(session['utilisateur_id'], nouveau_mdp)

        # on met à jour la session pour que le nom s'affiche correctement partout
        session['nom'] = nom
        flash('Profil mis à jour !', 'succes')
        return redirect(url_for('utilisateurs.profil'))

    return render_template('modifier_profil.html', utilisateur=user)


@utilisateurs_bp.route('/profil/supprimer', methods=['POST'])
@login_requis
def supprimer_compte():
    supprimer_utilisateur(session['utilisateur_id'])
    session.clear()
    flash('Compte supprimé. À bientôt peut-être !', 'succes')
    return redirect(url_for('auth.connexion'))
