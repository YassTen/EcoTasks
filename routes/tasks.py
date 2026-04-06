# routes/tasks.py - Tout le CRUD des tâches écologiques + dashboard

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.task import (
    creer_tache, get_taches, get_tache,
    modifier_tache, supprimer_tache, basculer_statut,
    stats_utilisateur, CATEGORIES
)
from utils import login_requis

taches_bp = Blueprint('taches', __name__)


@taches_bp.route('/tableau-de-bord')
@login_requis
def tableau_de_bord():
    user_id = session['utilisateur_id']
    filtre = request.args.get('filtre')  # None si pas de param -> affiche tout

    taches = get_taches(user_id, filtre)
    stats = stats_utilisateur(user_id)

    return render_template(
        'tableau_de_bord.html',
        taches=taches,
        stats=stats,
        filtre_actif=filtre,
        categories=CATEGORIES
    )


@taches_bp.route('/taches/ajouter', methods=['POST'])
@login_requis
def ajouter_tache():
    titre = request.form.get('titre', '').strip()
    description = request.form.get('description', '').strip()
    categorie = request.form.get('categorie', 'Autre')

    if not titre:
        flash('Il faut au moins un titre !', 'erreur')
        return redirect(url_for('taches.tableau_de_bord'))

    if len(titre) > 200:
        flash('Le titre est trop long (200 caractères max).', 'erreur')
        return redirect(url_for('taches.tableau_de_bord'))

    creer_tache(titre, description, categorie, session['utilisateur_id'])
    flash('Action ajoutée !', 'succes')
    return redirect(url_for('taches.tableau_de_bord'))


@taches_bp.route('/taches/<int:tache_id>/basculer', methods=['POST'])
@login_requis
def basculer(tache_id):
    tache = get_tache(tache_id)

    # sécurité : on vérifie que la tâche appartient bien à l'utilisateur connecté
    if not tache or tache['utilisateur_id'] != session['utilisateur_id']:
        flash('Tâche introuvable.', 'erreur')
        return redirect(url_for('taches.tableau_de_bord'))

    basculer_statut(tache_id)
    return redirect(url_for('taches.tableau_de_bord'))


@taches_bp.route('/taches/<int:tache_id>/modifier', methods=['GET', 'POST'])
@login_requis
def modifier(tache_id):
    tache = get_tache(tache_id)

    if not tache or tache['utilisateur_id'] != session['utilisateur_id']:
        flash('Tâche introuvable.', 'erreur')
        return redirect(url_for('taches.tableau_de_bord'))

    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        description = request.form.get('description', '').strip()
        categorie = request.form.get('categorie', 'Autre')

        if not titre:
            flash('Le titre ne peut pas être vide.', 'erreur')
            return render_template('modifier_tache.html', tache=tache, categories=CATEGORIES)

        modifier_tache(tache_id, titre, description, categorie)
        flash('Tâche modifiée.', 'succes')
        return redirect(url_for('taches.tableau_de_bord'))

    return render_template('modifier_tache.html', tache=tache, categories=CATEGORIES)


@taches_bp.route('/taches/<int:tache_id>/supprimer', methods=['POST'])
@login_requis
def supprimer(tache_id):
    tache = get_tache(tache_id)

    if not tache or tache['utilisateur_id'] != session['utilisateur_id']:
        flash('Tâche introuvable.', 'erreur')
        return redirect(url_for('taches.tableau_de_bord'))

    supprimer_tache(tache_id)
    flash('Tâche supprimée.', 'succes')
    return redirect(url_for('taches.tableau_de_bord'))
