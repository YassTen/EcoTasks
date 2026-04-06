# models/user.py - Tout ce qui touche aux utilisateurs en base
# Le hachage se fait avec bcrypt (plus sûr que md5/sha256 pour les mots de passe)

import bcrypt
from database import get_db


def creer_utilisateur(nom, email, mot_de_passe, role='utilisateur'):
    """Inscrit un nouvel utilisateur. Retourne True si OK, False si l'email est déjà pris."""
    # bcrypt attend des bytes, pas des strings
    sel = bcrypt.gensalt()
    mdp_hash = bcrypt.hashpw(mot_de_passe.encode('utf-8'), sel)

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)',
            (nom, email, mdp_hash.decode('utf-8'), role)
        )
        conn.commit()
        return True
    except Exception:
        # en général c'est une erreur UNIQUE constraint sur l'email
        conn.rollback()
        return False
    finally:
        conn.close()


def verifier_identifiants(email, mot_de_passe):
    """Vérifie email + mdp, retourne l'utilisateur si c'est bon, None sinon."""
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM utilisateurs WHERE email = ?', (email,)
    ).fetchone()
    conn.close()

    if not user:
        return None

    # checkpw compare le mdp en clair avec le hash stocké
    mdp_ok = bcrypt.checkpw(
        mot_de_passe.encode('utf-8'),
        user['mot_de_passe'].encode('utf-8')
    )
    return user if mdp_ok else None


def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM utilisateurs WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user


def get_user_par_email(email):
    conn = get_db()
    user = conn.execute('SELECT * FROM utilisateurs WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user


def modifier_utilisateur(user_id, nom, email):
    conn = get_db()
    try:
        conn.execute(
            'UPDATE utilisateurs SET nom = ?, email = ? WHERE id = ?',
            (nom, email, user_id)
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def changer_mot_de_passe(user_id, nouveau_mdp):
    mdp_hash = bcrypt.hashpw(nouveau_mdp.encode('utf-8'), bcrypt.gensalt())
    conn = get_db()
    conn.execute(
        'UPDATE utilisateurs SET mot_de_passe = ? WHERE id = ?',
        (mdp_hash.decode('utf-8'), user_id)
    )
    conn.commit()
    conn.close()


def supprimer_utilisateur(user_id):
    # les tâches associées sont supprimées automatiquement grâce au CASCADE
    conn = get_db()
    conn.execute('DELETE FROM utilisateurs WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


def lister_utilisateurs():
    """Pour le panel admin : liste tous les utilisateurs triés par date."""
    conn = get_db()
    users = conn.execute(
        'SELECT id, nom, email, role, date_creation FROM utilisateurs ORDER BY date_creation DESC'
    ).fetchall()
    conn.close()
    return users


def compter_utilisateurs():
    conn = get_db()
    nb = conn.execute('SELECT COUNT(*) as nb FROM utilisateurs').fetchone()['nb']
    conn.close()
    return nb


def changer_role(user_id, nouveau_role):
    """Passe un utilisateur en admin ou l'inverse."""
    conn = get_db()
    conn.execute('UPDATE utilisateurs SET role = ? WHERE id = ?', (nouveau_role, user_id))
    conn.commit()
    conn.close()
