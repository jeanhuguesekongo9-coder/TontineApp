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
        flash("Votre dossier doit etre approuve avant de rejoindre une tontine.", "warning")
        return redirect(url_for("kyc.statut"))
    tontine = Tontine.query.get_or_404(tontine_id)
    if tontine.statut != "recrutement":
        flash("Cette tontine n accepte plus de membres.", "warning")
        return redirect(url_for("tontines.liste"))
    if tontine.nombre_membres >= tontine.max_membres:
        flash("Cette tontine est complete.", "warning")
        return redirect(url_for("tontines.liste"))
    deja = MembreTontine.query.filter_by(user_id=current_user.id, tontine_id=tontine_id).first()
    if deja:
        flash("Vous êtes déjà membre.", "info")
        return redirect(url_for("tontines.detail", tontine_id=tontine_id))
    revenu = current_user.profil.revenu_mensuel or 0
    if revenu < tontine.montant_panier * 1.5:
        flash(f"Revenu insuffisant pour ce panier (minimum {tontine.montant_panier * 1.5:,.0f} FCFA/mois).", "danger")
        return redirect(url_for("tontines.liste"))
    if request.method == "POST":
        if not request.form.get("accepter_contrat"):
            flash("Vous devez accepter les termes du contrat.", "danger")
            return render_template("tontines/rejoindre.html", tontine=tontine)
        membre = MembreTontine(user_id=current_user.id, tontine_id=tontine_id)
        db.session.add(membre)
        tontine.nombre_membres += 1
        notif = Notification(user_id=current_user.id,
            titre="Adhesion confirmee",
            message=f"Vous avez rejoint la tontine {tontine.nom}.",
            type_notif="success",
            lien=url_for("tontines.mes_tontines"))
        db.session.add(notif)
        db.session.commit()
        AuditLog.log(current_user.id, "rejoindre_tontine", f"Tontine: {tontine.code}", ip=request.remote_addr)
        db.session.commit()
        flash(f"Felicitations ! Vous avez rejoint {tontine.nom}.", "success")
        return redirect(url_for("tontines.mes_tontines"))
    return render_template("tontines/rejoindre.html", tontine=tontine)

@tontines.route("/detail/<int:tontine_id>")
@login_required
def detail(tontine_id):
    tontine = Tontine.query.get_or_404(tontine_id)
    membres = MembreTontine.query.filter_by(tontine_id=tontine_id).all()
    mon_membership = MembreTontine.query.filter_by(user_id=current_user.id, tontine_id=tontine_id).first()
    mes_paiements = Paiement.query.filter_by(user_id=current_user.id, tontine_id=tontine_id).all() if mon_membership else []
    return render_template("tontines/detail.html",
        tontine=tontine, membres=membres,
        mon_membership=mon_membership,
        mes_paiements=mes_paiements)

@tontines.route("/mes-tontines")
@login_required
def mes_tontines():
    memberships = MembreTontine.query.filter_by(user_id=current_user.id).all()
    return render_template("tontines/mes_tontines.html", memberships=memberships)

