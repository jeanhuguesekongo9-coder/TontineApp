# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
import os
from ..models import db, Solde, Recharge, Transaction, Notification

paiements = Blueprint("paiements", __name__)

TAUX_FRAIS = 0.015  # 1.5% de frais sur chaque recharge

RESEAUX = {
    "wave_sn": {
        "nom": "Wave Sénégal",
        "type": "link",
        "base_url": "https://pay.wave.com/m/M_sn_XhdrMMWqgQ6I/c/sn/?amount=",
        "numero": "+221 78 538 53 10",
        "couleur": "#1DC8EE",
    },
    "wave_ci": {
        "nom": "Wave Côte d'Ivoire",
        "type": "link",
        "base_url": "https://pay.wave.com/m/M_sn_XhdrMMWqgQ6I/c/sn/?amount=",
        "numero": "+225 05 84 02 23 23",
        "couleur": "#1DC8EE",
    },
    "orange_sn": {
        "nom": "Orange Money Sénégal",
        "type": "ussd",
        "ussd_pattern": "*144*1*221785385310*{montant}#",
        "numero": "+221 78 538 53 10",
        "couleur": "#FF6600",
    },
    "orange_ci": {
        "nom": "Orange Money CI",
        "type": "ussd",
        "ussd_pattern": "*144*1*2250708224241*{montant}#",
        "numero": "+225 07 08 22 42 41",
        "couleur": "#FF6600",
    },
    "mtn_ci": {
        "nom": "MTN MoMo CI",
        "type": "ussd",
        "ussd_pattern": "*133*1*2250584022323*{montant}#",
        "numero": "+225 05 84 02 23 23",
        "couleur": "#FFCC00",
    },
}

def get_ou_creer_solde(user_id):
    solde = Solde.query.filter_by(user_id=user_id).first()
    if not solde:
        solde = Solde(user_id=user_id, montant=0.0)
        db.session.add(solde)
        db.session.commit()
    return solde

def calculer_frais(montant):
    frais = round(montant * TAUX_FRAIS)
    return {"net": montant, "frais": frais, "total": montant + frais}

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
        montant_net = float(request.form.get("montant", 0))
        reseau = request.form.get("reseau", "")
        numero = request.form.get("numero_telephone", "").strip()
        reference_transaction = request.form.get("reference_transaction", "").strip()
        capture = request.files.get("capture")
        if montant_net < 1000:
            flash("Montant minimum 1 000 FCFA.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not reseau or reseau not in RESEAUX:
            flash("Réseau invalide.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not numero:
            flash("Numéro de téléphone obligatoire.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not capture or not capture.filename:
            flash("La capture du transfert est obligatoire.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        ext = capture.filename.rsplit('.', 1)[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'pdf']:
            flash("Format capture invalide. JPG, PNG ou PDF uniquement.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        import secrets
        capture_filename = f"capture_{secrets.token_hex(8)}.{ext}"
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'captures')
        os.makedirs(upload_dir, exist_ok=True)
        capture.save(os.path.join(upload_dir, capture_filename))
        calc = calculer_frais(montant_net)
        recharge = Recharge(
            reference=Recharge.generer_reference(),
            user_id=current_user.id,
            montant=montant_net,
            reseau=reseau,
            numero_telephone=numero,
            reference_transaction=reference_transaction or "A_VERIFIER",
            statut="en_attente",
            note_admin=capture_filename
        )
        db.session.add(recharge)
        db.session.commit()
        notif = Notification(
            user_id=current_user.id,
            titre="Recharge en attente de validation",
            message=f"Votre recharge de {montant_net:,.0f} FCFA nets (+ {calc['frais']:,.0f} FCFA de frais) via {RESEAUX[reseau]['nom']} est en cours de vérification. Validation sous 24h maximum.",
            type_notif="info",
            lien=url_for("paiements.dashboard")
        )
        db.session.add(notif)
        db.session.commit()
        flash(f"Recharge de {montant_net:,.0f} FCFA soumise avec succès ! Vérification par notre équipe sous 24h.", "success")
        return redirect(url_for("paiements.dashboard"))
    return render_template("paiements/recharger.html", reseaux=RESEAUX)

@paiements.route("/facture/<string:reference>")
@login_required
def facture(reference):
    transaction = Transaction.query.filter_by(reference=reference, user_id=current_user.id).first_or_404()
    return render_template("paiements/facture.html", transaction=transaction)

@paiements.route("/ma-tontine")
@login_required
def ma_tontine():
    from ..models import MembreTontine, Penalite
    memberships = MembreTontine.query.filter_by(user_id=current_user.id).all()
    penalites_actives = Penalite.query.filter(
        Penalite.user_id == current_user.id,
        Penalite.statut.in_(["en_cours", "mise_en_demeure"])
    ).all()
    return render_template("paiements/ma_tontine.html",
        memberships=memberships,
        penalites_actives=penalites_actives)
