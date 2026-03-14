import os
os.makedirs("app/paiements", exist_ok=True)
open("app/paiements/__init__.py", "w", encoding="utf-8").write("""# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from ..models import db, Solde, Recharge, Transaction, Notification

paiements = Blueprint("paiements", __name__)

RESEAUX = {
    "wave_sn": {"nom": "Wave Senegal", "numero": "+221 77 XXX XX XX", "flag": "🇸🇳"},
    "wave_ci": {"nom": "Wave Cote d Ivoire", "numero": "+225 07 XXX XX XX", "flag": "🇨🇮"},
    "orange_sn": {"nom": "Orange Money Senegal", "numero": "+221 77 XXX XX XX", "flag": "🇸🇳"},
    "orange_ci": {"nom": "Orange Money CI", "numero": "+225 07 XXX XX XX", "flag": "🇨🇮"},
    "mtn_ci": {"nom": "MTN CI", "numero": "+225 05 XXX XX XX", "flag": "🇨🇮"},
}

def get_ou_creer_solde(user_id):
    solde = Solde.query.filter_by(user_id=user_id).first()
    if not solde:
        solde = Solde(user_id=user_id, montant=0.0)
        db.session.add(solde)
        db.session.commit()
    return solde

@paiements.route("/")
@login_required
def dashboard():
    solde = get_ou_creer_solde(current_user.id)
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(20).all()
    recharges = Recharge.query.filter_by(user_id=current_user.id).order_by(Recharge.created_at.desc()).limit(10).all()
    return render_template("paiements/dashboard.html", solde=solde, transactions=transactions, recharges=recharges, reseaux=RESEAUX)

@paiements.route("/recharger", methods=["GET", "POST"])
@login_required
def recharger():
    if request.method == "POST":
        montant = float(request.form.get("montant", 0))
        reseau = request.form.get("reseau", "")
        numero = request.form.get("numero_telephone", "").strip()
        reference_transaction = request.form.get("reference_transaction", "").strip()
        if montant < 1000:
            flash("Montant minimum 1 000 FCFA.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not reseau or reseau not in RESEAUX:
            flash("Reseau invalide.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not numero or not reference_transaction:
            flash("Numero et reference de transaction obligatoires.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        recharge = Recharge(
            reference=Recharge.generer_reference(),
            user_id=current_user.id,
            montant=montant,
            reseau=reseau,
            numero_telephone=numero,
            reference_transaction=reference_transaction,
            statut="en_attente"
        )
        db.session.add(recharge)
        db.session.commit()
        notif = Notification(
            user_id=current_user.id,
            titre="Recharge en attente",
            message=f"Votre recharge de {montant:,.0f} FCFA via {RESEAUX[reseau]['nom']} est en cours de validation.",
            type_notif="info",
            lien=url_for("paiements.dashboard")
        )
        db.session.add(notif)
        db.session.commit()
        flash("Recharge soumise ! Validation sous 24h.", "success")
        return redirect(url_for("paiements.dashboard"))
    return render_template("paiements/recharger.html", reseaux=RESEAUX)

@paiements.route("/facture/<string:reference>")
@login_required
def facture(reference):
    transaction = Transaction.query.filter_by(reference=reference, user_id=current_user.id).first_or_404()
    return render_template("paiements/facture.html", transaction=transaction)
""")
print("OK!")
