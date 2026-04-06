# routes/auth.py - Inscription, connexion, déconnexion
# Gère tout le flow d'authentification avec bcrypt + sessions Flask

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import creer_utilisateur, verifier_identifiants, get_user_par_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    # si déjà connecté, pas besoin de s'inscrire
    if 'utilisateur_id' in session:
        return redirect(url_for('taches.tableau_de_bord'))

    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip().lower()
        mdp = request.form.get('mot_de_passe', '')
        confirm = request.form.get('confirmation', '')

        # Validations basiques - on pourrait faire plus propre avec WTForms
        # mais c'est overkill pour ce projet
        if not nom or not email or not mdp:
            flash('Tous les champs sont obligatoires.', 'erreur')
            return render_template('inscription.html', nom=nom, email=email)

        if len(mdp) < 6:
            flash('Le mot de passe doit faire au moins 6 caractères.', 'erreur')
            return render_template('inscription.html', nom=nom, email=email)

        if mdp != confirm:
            flash('Les mots de passe ne correspondent pas.', 'erreur')
            return render_template('inscription.html', nom=nom, email=email)

        # vérif si l'email est déjà pris avant d'essayer l'INSERT
        if get_user_par_email(email):
            flash('Un compte existe déjà avec cet email.', 'erreur')
            return render_template('inscription.html', nom=nom, email=email)

        if creer_utilisateur(nom, email, mdp):
            flash('Compte créé ! Vous pouvez vous connecter.', 'succes')
            return redirect(url_for('auth.connexion'))
        else:
            flash('Erreur lors de la création du compte.', 'erreur')

    return render_template('inscription.html')


@auth_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if 'utilisateur_id' in session:
        return redirect(url_for('taches.tableau_de_bord'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        mdp = request.form.get('mot_de_passe', '')

        if not email or not mdp:
            flash('Remplissez tous les champs.', 'erreur')
            return render_template('connexion.html', email=email)

        user = verifier_identifiants(email, mdp)
        if user:
            # on stocke les infos utiles en session pour éviter de requêter la BDD à chaque page
            session['utilisateur_id'] = user['id']
            session['nom'] = user['nom']
            session['role'] = user['role']
            flash(f'Bienvenue {user["nom"]} !', 'succes')
            return redirect(url_for('taches.tableau_de_bord'))
        else:
            flash('Email ou mot de passe incorrect.', 'erreur')
            return render_template('connexion.html', email=email)

    return render_template('connexion.html')


@auth_bp.route('/deconnexion')
def deconnexion():
    session.clear()
    flash('Déconnecté.', 'succes')
    return redirect(url_for('auth.connexion'))
