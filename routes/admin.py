# routes/admin.py - Panel admin pour gérer les utilisateurs

from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.user import lister_utilisateurs, supprimer_utilisateur, compter_utilisateurs, changer_role
from models.task import stats_globales
from utils import admin_requis

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@admin_requis
def panel_admin():
    users = lister_utilisateurs()
    nb_users = compter_utilisateurs()
    stats = stats_globales()

    return render_template('admin.html',
                           utilisateurs=users,
                           nb_utilisateurs=nb_users,
                           stats_taches=stats)


@admin_bp.route('/admin/utilisateurs/<int:user_id>/promouvoir', methods=['POST'])
@admin_requis
def promouvoir_admin(user_id):
    # on ne peut pas se modifier soi-même ici (pas de sens)
    if user_id == session['utilisateur_id']:
        flash('Vous ne pouvez pas modifier votre propre rôle.', 'erreur')
        return redirect(url_for('admin.panel_admin'))

    changer_role(user_id, 'admin')
    flash('Utilisateur promu administrateur.', 'succes')
    return redirect(url_for('admin.panel_admin'))


@admin_bp.route('/admin/utilisateurs/<int:user_id>/retrograder', methods=['POST'])
@admin_requis
def retrograder_user(user_id):
    if user_id == session['utilisateur_id']:
        flash('Vous ne pouvez pas vous rétrograder vous-même.', 'erreur')
        return redirect(url_for('admin.panel_admin'))

    changer_role(user_id, 'utilisateur')
    flash('Administrateur rétrogradé en utilisateur.', 'succes')
    return redirect(url_for('admin.panel_admin'))


@admin_bp.route('/admin/utilisateurs/<int:user_id>/supprimer', methods=['POST'])
@admin_requis
def supprimer_user(user_id):
    # empêcher l'admin de se supprimer lui-même par erreur
    if user_id == session['utilisateur_id']:
        flash('Vous ne pouvez pas supprimer votre propre compte ici.', 'erreur')
        return redirect(url_for('admin.panel_admin'))

    supprimer_utilisateur(user_id)
    flash('Utilisateur supprimé.', 'succes')
    return redirect(url_for('admin.panel_admin'))
