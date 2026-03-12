import os, sys
sys.path.insert(0, ".")
os.environ.setdefault("FLASK_ENV", "production")

from app import create_app
from app.models import db, Utilisateur, Profil, KYC, Tontine, MembreTontine, Paiement, AuditLog, Notification

app = create_app()
with app.app_context():
    # Supprimer dans le bon ordre (respect des clés étrangères)
    Notification.query.delete()
    AuditLog.query.delete()
    Paiement.query.delete()
    MembreTontine.query.delete()
    Tontine.query.delete()
    KYC.query.delete()
    Profil.query.delete()
    # Supprimer tous les users SAUF l'admin
    Utilisateur.query.filter(Utilisateur.role != "admin").delete()
    db.session.commit()
    print("Base de donnees reinitalisee !")
    print(f"Utilisateurs restants : {Utilisateur.query.count()}")
    print(f"Tontines : {Tontine.query.count()}")
    print(f"KYC : {KYC.query.count()}")
