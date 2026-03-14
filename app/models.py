from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import secrets

db = SQLAlchemy()
bcrypt = Bcrypt()

class Utilisateur(UserMixin, db.Model):
    __tablename__ = "utilisateurs"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="membre")
    email_verifie = db.Column(db.Boolean, default=False)
    tel_verifie = db.Column(db.Boolean, default=False)
    kyc_valide = db.Column(db.Boolean, default=False)
    compte_actif = db.Column(db.Boolean, default=True)
    token_email = db.Column(db.String(100))
    token_email_expiry = db.Column(db.DateTime)
    code_sms = db.Column(db.String(6))
    code_sms_expiry = db.Column(db.DateTime)
    tentatives_sms = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profil = db.relationship("Profil", backref="utilisateur", uselist=False, cascade="all, delete-orphan")
    kyc = db.relationship("KYC", backref="utilisateur", uselist=False, cascade="all, delete-orphan", foreign_keys="KYC.user_id")
    memberships = db.relationship("MembreTontine", backref="utilisateur", lazy="dynamic")
    paiements = db.relationship("Paiement", backref="utilisateur", lazy="dynamic")
    audit_logs = db.relationship("AuditLog", backref="utilisateur", lazy="dynamic")

    def set_password(self, password):
        self.mot_de_passe = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.mot_de_passe, password)

    def generer_token_email(self):
        self.token_email = secrets.token_urlsafe(32)
        self.token_email_expiry = datetime.utcnow() + timedelta(hours=24)
        return self.token_email

    def generer_code_sms(self):
        import random
        self.code_sms = str(random.randint(1000, 9999))
        self.code_sms_expiry = datetime.utcnow() + timedelta(minutes=10)
        self.tentatives_sms = 0
        return self.code_sms

    def verifier_code_sms(self, code):
        if self.tentatives_sms >= 3:
            return False, "Trop de tentatives. Demandez un nouveau code."
        if not self.code_sms_expiry or datetime.utcnow() > self.code_sms_expiry:
            return False, "Code expire."
        if self.code_sms != code:
            self.tentatives_sms += 1
            return False, "Code incorrect."
        return True, "OK"

class Profil(db.Model):
    __tablename__ = "profils"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    ville = db.Column(db.String(100))
    pays = db.Column(db.String(100))
    adresse = db.Column(db.String(255))
    profession = db.Column(db.String(150))
    employeur = db.Column(db.String(150))
    revenu_mensuel = db.Column(db.Float)
    photo_profil = db.Column(db.String(255))
    rib = db.Column(db.String(34))
    banque = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

class KYC(db.Model):
    __tablename__ = "kyc"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    doc_identite = db.Column(db.String(255))
    type_doc = db.Column(db.String(50))
    doc_identite2 = db.Column(db.String(255))
    bulletin_salaire = db.Column(db.String(255))
    statut = db.Column(db.String(30), default="en_attente")
    note_admin = db.Column(db.Text)
    verifie_par = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"))
    verifie_le = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    STATUTS = {
        "en_attente": ("En attente", "warning"),
        "en_cours": ("En cours", "info"),
        "approuve": ("Approuve", "success"),
        "rejete": ("Rejete", "danger"),
    }

class Tontine(db.Model):
    __tablename__ = "tontines"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    nom = db.Column(db.String(150), nullable=False)
    montant_panier = db.Column(db.Float, nullable=False)
    nombre_membres = db.Column(db.Integer, default=0)
    min_membres = db.Column(db.Integer, default=5)
    max_membres = db.Column(db.Integer, default=10)
    statut = db.Column(db.String(30), default="recrutement")
    date_debut = db.Column(db.DateTime)
    jour_collecte = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    createur_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    membres = db.relationship("MembreTontine", backref="tontine", lazy="dynamic", cascade="all, delete-orphan")
    paiements = db.relationship("Paiement", backref="tontine", lazy="dynamic")
    contrats = db.relationship("Contrat", backref="tontine", lazy="dynamic")

    @staticmethod
    def generer_code():
        return "T" + secrets.token_hex(4).upper()

    @property
    def places_restantes(self):
        return self.max_membres - self.nombre_membres

    @property
    def peut_demarrer(self):
        return self.nombre_membres >= self.min_membres

    STATUTS = {
        "recrutement": ("Recrutement", "warning"),
        "en_cours": ("En cours", "success"),
        "terminee": ("Terminee", "info"),
        "suspendue": ("Suspendue", "danger"),
    }

class MembreTontine(db.Model):
    __tablename__ = "membres_tontines"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=False)
    ordre_collecte = db.Column(db.Integer)
    a_recu = db.Column(db.Boolean, default=False)
    statut = db.Column(db.String(20), default="actif")
    date_adhesion = db.Column(db.DateTime, default=datetime.utcnow)
    contrat_signe = db.Column(db.Boolean, default=False)
    contrat_signe_le = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint("user_id", "tontine_id", name="uq_user_tontine"),)

class Paiement(db.Model):
    __tablename__ = "paiements"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    type_paiement = db.Column(db.String(30))
    mois_reference = db.Column(db.String(7))
    statut = db.Column(db.String(20), default="en_attente")
    date_echeance = db.Column(db.DateTime)
    date_paiement = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generer_reference():
        return "PAY" + secrets.token_hex(6).upper()

class Contrat(db.Model):
    __tablename__ = "contrats"
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    tontine_id = db.Column(db.Integer, db.ForeignKey("tontines.id"), nullable=False)
    fichier_pdf = db.Column(db.String(255))
    hash_contrat = db.Column(db.String(64))
    signe = db.Column(db.Boolean, default=False)
    signe_le = db.Column(db.DateTime)
    ip_signature = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="contrats", foreign_keys=[user_id])

    @staticmethod
    def generer_reference():
        return "CTR" + secrets.token_hex(6).upper()

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"))
    action = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    @staticmethod
    def log(user_id, action, detail=None, ip=None, ua=None):
        entry = AuditLog(user_id=user_id, action=action, detail=detail, ip_address=ip, user_agent=ua)
        db.session.add(entry)

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    titre = db.Column(db.String(150))
    message = db.Column(db.Text)
    type_notif = db.Column(db.String(30))
    lue = db.Column(db.Boolean, default=False)
    lien = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", backref="notifications", foreign_keys=[user_id])

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
