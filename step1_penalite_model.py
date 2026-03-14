import os

# ============================================================
# ETAPE 1 : Ajouter le modele Penalite dans models.py
# ============================================================
content = open("app/models.py", encoding="utf-8-sig", errors="replace").read()

nouveau_modele = """
class Penalite(db.Model):
    __tablename__ = "penalites"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=False)
    montant_du = db.Column(db.Float, nullable=False)
    montant_penalite = db.Column(db.Float, nullable=False)
    taux = db.Column(db.Float, default=1.5)
    mois_reference = db.Column(db.String(7), nullable=False)
    statut = db.Column(db.String(20), default="en_cours")
    mois_impaye = db.Column(db.Integer, default=1)
    note_admin = db.Column(db.Text)
    regularise_le = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="penalites", foreign_keys=[user_id])
    tontine = db.relationship("Tontine", backref="penalites", foreign_keys=[tontine_id])

    @staticmethod
    def generer_reference():
        return "PEN" + secrets.token_hex(6).upper()

    @property
    def en_poursuite(self):
        return self.mois_impaye >= 3
"""

# Ajouter apres la classe Transaction
content = content.rstrip() + "\n" + nouveau_modele
open("app/models.py", "w", encoding="utf-8").write(content)
print("OK! Modele Penalite ajoute")
