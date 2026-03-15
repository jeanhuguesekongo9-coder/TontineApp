texte = """# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from ..models import db, Tontine, MembreTontine, Paiement, AuditLog, Notification

tontines = Blueprint("tontines", __name__)

@tontines.route("/")
@login_required
def liste():
    tontines_dispo = Tontine.query.filter_by(statut="recrutement").order_by(Tontine.montant_panier).all()
    mes_ids = [m.tontine_id for m in MembreTontine.query.filter_by(user_id=current_user.id).all()]
    return render_template("tontines/liste.html",
        tontines=tontines_dispo,
        mes_ids=mes_ids,
        paniers=current_app.config["PANIERS"])

@tontines.route("/rejoindre/<int:tontine_id>", methods=["GET", "POST"])
@login_required
def rejoindre(tontine_id):
    if not current_user.kyc_valide:
        flash("Votre dossier KYC doit être approuvé avant de rejoindre une tontine.", "warning")
        return redirect(url_for("kyc.statut"))
    tontine = Tontine.query.get_or_404(tontine_id)
    if tontine.statut != "recrutement":
        flash("Cette tontine n'accepte plus de membres.", "warning")
        return redirect(url_for("tontines.liste"))
    if tontine.nombre_membres >= tontine.max_membres:
        flash("Cette tontine est complète.", "warning")
        return redirect(url_for("tontines.liste"))
    deja = MembreTontine.query.filter_by(user_id=current_user.id, tontine_id=tontine_id).first()
    if deja:
        flash("Vous êtes déjà membre de cette tontine.", "info")
        return redirect(url_for("tontines.detail", tontine_id=tontine_id))
    revenu = current_user.profil.revenu_mensuel or 0
    if revenu < tontine.montant_panier * 1.5:
        flash(f"Revenu insuffisant pour ce panier (minimum {tontine.montant_panier * 1.5:,.0f} FCFA/mois).", "danger")
        return redirect(url_for("tontines.liste"))
    # Redirection obligatoire vers la signature du contrat
    return redirect(url_for("contrats.voir_contrat", tontine_id=tontine_id))

@tontines.route("/detail/<int:tontine_id>")
@login_required
def detail(tontine_id):
    tontine = Tontine.query.get_or_404(tontine_id)
    membres = MembreTontine.query.filter_by(tontine_id=tontine_id).all()
    mon_membership = MembreTontine.query.filter_by(user_id=current_user.id, tontine_id=tontine_id).first()
    mes_paiements = Paiement.query.filter_by(user_id=current_user.id, tontine_id=tontine_id).all() if mon_membership else []
    return render_template("tontines/detail.html",
        tontine=tontine,
        membres=membres,
        mon_membership=mon_membership,
        mes_paiements=mes_paiements)

@tontines.route("/mes-tontines")
@login_required
def mes_tontines():
    memberships = MembreTontine.query.filter_by(user_id=current_user.id).all()
    return render_template("tontines/mes_tontines.html", memberships=memberships)
"""
open("app/tontines/__init__.py", "w", encoding="utf-8").write(texte)
print("OK tontines/__init__.py réécrit proprement!")
