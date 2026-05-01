"""Script temporaire pour inspecter la base de donnees."""
import sqlite3

conn = sqlite3.connect('ecotasks.db')
conn.row_factory = sqlite3.Row

print("=== TABLES ===")
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    print(f"  - {t['name']}")

print("\n=== UTILISATEURS ===")
users = conn.execute("SELECT id, nom, email, role, date_creation FROM utilisateurs").fetchall()
if users:
    for u in users:
        print(f"  [{u['id']}] {u['nom']} | {u['email']} | {u['role']} | {u['date_creation']}")
else:
    print("  (aucun utilisateur)")

print("\n=== TACHES ===")
taches = conn.execute("SELECT id, titre, categorie, est_accomplie, utilisateur_id FROM taches").fetchall()
if taches:
    for t in taches:
        etat = "OK" if t['est_accomplie'] else "a faire"
        print(f"  [{t['id']}] {t['titre']} | {t['categorie']} | {etat} | user_id={t['utilisateur_id']}")
else:
    print("  (aucune tache)")

print("\n=== INDEX ===")
idx = conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
for i in idx:
    print(f"  - {i['name']}")

conn.close()
