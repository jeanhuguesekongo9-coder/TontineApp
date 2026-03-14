content = open("app/models.py", encoding="utf-8-sig", errors="replace").read()

nouveaux_modeles = """

class Solde(db.Model):
    __tablename__ = "soldes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False, unique=True)
    montant = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref=db.backref("solde", uselist=False))

class Recharge(db.Model):
    __tablename__ = "recharges"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    reseau = db.Column(db.String(30), nullable=False)  # wave_sn, wave_ci, orange_sn, orange_ci, mtn_ci
    numero_telephone = db.Column(db.String(20))
    reference_transaction = db.Column(db.String(100))
    statut = db.Column(db.String(20), default="en_attente")  # en_attente, valide, rejete
    note_admin = db.Column(db.Text)
    valide_par = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"))
    valide_le = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="recharges", foreign_keys=[user_id])

    @staticmethod
    def generer_reference():
        return "RCH" + secrets.token_hex(6).upper()

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=True)
    type_transaction = db.Column(db.String(30), nullable=False)  # recharge, cotisation, reception, retrait
    montant = db.Column(db.Float, nullable=False)
    sens = db.Column(db.String(10), nullable=False)  # credit, debit
    solde_avant = db.Column(db.Float)
    solde_apres = db.Column(db.Float)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="transactions", foreign_keys=[user_id])

    @staticmethod
    def generer_reference():
        return "TRX" + secrets.token_hex(6).upper()
"""

content = content.rstrip() + nouveaux_modeles
open("app/models.py", "w", encoding="utf-8").write(content)
print("OK!")
