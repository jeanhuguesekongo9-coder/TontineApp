import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'

# 1. Ajouter FondsGarantie dans models.py
content = open("app/models.py", encoding="utf-8-sig", errors="replace").read()

if "FondsGarantie" not in content:
    nouveau_modele = """
class FondsGarantie(db.Model):
    __tablename__ = "fonds_garantie"
    id = db.Column(db.Integer, primary_key=True)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=False, unique=True)
    montant = db.Column(db.Float, default=0.0)
    seuil_activation = db.Column(db.Float, default=0.0)
    actif = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tontine = db.relationship("Tontine", backref=db.backref("fonds_garantie", uselist=False))

class FraisTransaction(db.Model):
    __tablename__ = "frais_transactions"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=True)
    type_frais = db.Column(db.String(30), nullable=False)
    montant_base = db.Column(db.Float, nullable=False)
    taux = db.Column(db.Float, nullable=False)
    montant_frais = db.Column(db.Float, nullable=False)
    montant_fonds_garantie = db.Column(db.Float, default=0.0)
    montant_tontinesecure = db.Column(db.Float, default=0.0)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="frais_transactions", foreign_keys=[user_id])

    @staticmethod
    def generer_reference():
        return "FRS" + secrets.token_hex(6).upper()

class FraisAnnuel(db.Model):
    __tablename__ = "frais_annuels"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.String(20), default="en_attente")
    preleve_le = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="frais_annuels", foreign_keys=[user_id])

    @staticmethod
    def generer_reference():
        return "FAN" + secrets.token_hex(6).upper()
"""
    content = content.rstrip() + "\n" + nouveau_modele
    open("app/models.py", "w", encoding="utf-8").write(content)
    print("OK modèles financiers ajoutés!")
else:
    print("Déjà présent!")

from app import create_app
app = create_app('development')
with app.app_context():
    from app.models import db
    db.create_all()
    print("OK migration BDD!")

    from app.models import MembreTontine
    membres_sans_ordre = MembreTontine.query.filter(MembreTontine.ordre_collecte == None).all()
    for i, m in enumerate(membres_sans_ordre):
        m.ordre_collecte = i + 1
    db.session.commit()
    print(f"OK ordre_collecte corrigé pour {len(membres_sans_ordre)} membre(s)!")

    from app.models import Tontine, FondsGarantie
    tontines_list = Tontine.query.all()
    for t in tontines_list:
        if not t.fonds_garantie:
            fg = FondsGarantie(
                tontine_id=t.id,
                montant=0.0,
                seuil_activation=round(t.montant_panier * 0.20, 2),
                actif=False
            )
            db.session.add(fg)
    db.session.commit()
    print("OK fonds de garantie créés!")
