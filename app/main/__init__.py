from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Tontine, MembreTontine, Paiement, Notification

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.tableau_de_bord"))
    return render_template("index.html")

@main.route("/tableau-de-bord")
@login_required
def tableau_de_bord():
    memberships = MembreTontine.query.filter_by(user_id=current_user.id).all()
    tontines_ids = [m.tontine_id for m in memberships]
    paiements_dus = Paiement.query.filter_by(user_id=current_user.id, statut="en_attente").all() if tontines_ids else []
    tontines_dispo = Tontine.query.filter_by(statut="recrutement").limit(3).all()
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5).all()
    return render_template("tableau_de_bord.html",
        memberships=memberships,
        paiements_dus=paiements_dus,
        tontines_dispo=tontines_dispo,
        notifs=notifs)

@main.route("/marquer-notification/<int:notif_id>")
@login_required
def marquer_notification(notif_id):
    from ..models import db
    notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first()
    if notif:
        notif.lue = True
        db.session.commit()
    return redirect(url_for("main.tableau_de_bord"))
