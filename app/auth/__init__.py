from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from ..models import db, Utilisateur, Profil, AuditLog

auth = Blueprint("auth", __name__)

@auth.route("/inscription", methods=["GET", "POST"])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for("main.tableau_de_bord"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("mot_de_passe", "")
        confirm = request.form.get("confirmer_mdp", "")
        if not email or not password:
            flash("Tous les champs sont requis.", "danger")
            return render_template("auth/inscription.html")
        if password != confirm:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return render_template("auth/inscription.html")
        if len(password) < 8:
            flash("Le mot de passe doit contenir au moins 8 caracteres.", "danger")
            return render_template("auth/inscription.html")
        if Utilisateur.query.filter_by(email=email).first():
            flash("Cet email est deja utilise.", "danger")
            return render_template("auth/inscription.html")
        user = Utilisateur(email=email)
        user.set_password(password)
        user.email_verifie = True
        db.session.add(user)
        db.session.commit()
        AuditLog.log(user.id, "inscription", f"Email: {email}", ip=request.remote_addr)
        db.session.commit()
        flash("Compte cree ! Completez maintenant votre profil.", "success")
        login_user(user)
        return redirect(url_for("auth.completer_profil"))
    return render_template("auth/inscription.html")

@auth.route("/email-envoye")
def email_envoye():
    return render_template("auth/email_envoye.html")

@auth.route("/verifier-email/<token>")
def verifier_email(token):
    user = Utilisateur.query.filter_by(token_email=token).first()
    if not user:
        flash("Lien invalide.", "danger")
        return redirect(url_for("auth.connexion"))
    user.email_verifie = True
    user.token_email = None
    db.session.commit()
    login_user(user)
    flash("Email confirme ! Completez votre profil.", "success")
    return redirect(url_for("auth.completer_profil"))

@auth.route("/connexion", methods=["GET", "POST"])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for("main.tableau_de_bord"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("mot_de_passe", "")
        user = Utilisateur.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Email ou mot de passe incorrect.", "danger")
            return render_template("auth/connexion.html")
        if not user.compte_actif:
            flash("Compte suspendu. Contactez le support.", "danger")
            return render_template("auth/connexion.html")
        user.last_login = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=request.form.get("souvenir") == "on")
        AuditLog.log(user.id, "connexion", ip=request.remote_addr)
        db.session.commit()
        if not user.profil:
            return redirect(url_for("auth.completer_profil"))
        if not user.tel_verifie:
            return redirect(url_for("auth.verifier_telephone"))
        if not user.kyc_valide:
            return redirect(url_for("kyc.soumettre"))
        return redirect(url_for("main.tableau_de_bord"))
    return render_template("auth/connexion.html")

@auth.route("/profil", methods=["GET", "POST"])
@login_required
def completer_profil():
    if current_user.profil:
        return redirect(url_for("auth.verifier_telephone"))
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        prenom = request.form.get("prenom", "").strip()
        date_naissance = request.form.get("date_naissance")
        telephone = request.form.get("telephone", "").strip()
        ville = request.form.get("ville", "").strip()
        pays = request.form.get("pays", "").strip()
        profession = request.form.get("profession", "").strip()
        employeur = request.form.get("employeur", "").strip()
        revenu = request.form.get("revenu_mensuel", 0)
        if not all([nom, prenom, date_naissance, telephone]):
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return render_template("auth/profil.html")
        if Profil.query.filter_by(telephone=telephone).first():
            flash("Ce numero de telephone est deja utilise.", "danger")
            return render_template("auth/profil.html")
        from datetime import date
        try:
            dob = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            age = (date.today() - dob).days // 365
            if age < 18:
                flash("Vous devez avoir au moins 18 ans.", "danger")
                return render_template("auth/profil.html")
        except ValueError:
            flash("Date de naissance invalide.", "danger")
            return render_template("auth/profil.html")
        profil = Profil(user_id=current_user.id, nom=nom, prenom=prenom,
            date_naissance=dob, telephone=telephone, ville=ville, pays=pays,
            profession=profession, employeur=employeur,
            revenu_mensuel=float(revenu) if revenu else None)
        db.session.add(profil)
        current_user.tel_verifie = True
        db.session.commit()
        flash("Profil enregistre ! Passez a la verification KYC.", "success")
        return redirect(url_for("kyc.soumettre"))
    return render_template("auth/profil.html")

@auth.route("/verifier-telephone", methods=["GET", "POST"])
@login_required
def verifier_telephone():
    if current_user.tel_verifie:
        return redirect(url_for("kyc.soumettre"))
    if request.method == "POST":
        current_user.tel_verifie = True
        db.session.commit()
        return redirect(url_for("kyc.soumettre"))
    return render_template("auth/verifier_telephone.html")

@auth.route("/renvoyer-code-sms")
@login_required
def renvoyer_code_sms():
    flash("Nouveau code envoye.", "info")
    return redirect(url_for("auth.verifier_telephone"))

@auth.route("/deconnexion")
@login_required
def deconnexion():
    AuditLog.log(current_user.id, "deconnexion", ip=request.remote_addr)
    db.session.commit()
    logout_user()
    flash("Vous avez ete deconnecte.", "info")
    return redirect(url_for("auth.connexion"))

@auth.route("/renvoyer-verification", methods=["GET", "POST"])
def renvoyer_verification():
    if request.method == "POST":
        flash("Si cet email existe, un lien a ete envoye.", "info")
        return redirect(url_for("auth.email_envoye"))
    return render_template("auth/email_envoye.html")
