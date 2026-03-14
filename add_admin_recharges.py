content = open("app/admin/__init__.py", encoding="utf-8-sig", errors="replace").read()

nouvelles_routes = """
@admin.route("/recharges")
@admin_requis
def gerer_recharges():
    from ..models import Recharge
    statut = request.args.get("statut", "en_attente")
    recharges = Recharge.query.filter_by(statut=statut).order_by(Recharge.created_at.desc()).all()
    RESEAUX = {
        "wave_sn": "Wave Senegal", "wave_ci": "Wave CI",
        "orange_sn": "Orange Senegal", "orange_ci": "Orange CI", "mtn_ci": "MTN CI"
    }
    return render_template("admin/recharges.html", recharges=recharges, statut=statut, RESEAUX=RESEAUX)

@admin.route("/recharges/<int:recharge_id>/valider", methods=["POST"])
@admin_requis
def valider_recharge(recharge_id):
    from ..models import Recharge, Solde, Transaction
    recharge = Recharge.query.get_or_404(recharge_id)
    if recharge.statut != "en_attente":
        flash("Cette recharge a deja ete traitee.", "warning")
        return redirect(url_for("admin.gerer_recharges"))
    solde = Solde.query.filter_by(user_id=recharge.user_id).first()
    if not solde:
        solde = Solde(user_id=recharge.user_id, montant=0.0)
        db.session.add(solde)
        db.session.flush()
    solde_avant = solde.montant
    solde.montant += recharge.montant
    recharge.statut = "valide"
    recharge.valide_par = current_user.id
    recharge.valide_le = datetime.utcnow()
    trx = Transaction(
        reference=Transaction.generer_reference(),
        user_id=recharge.user_id,
        type_transaction="recharge",
        montant=recharge.montant,
        sens="credit",
        solde_avant=solde_avant,
        solde_apres=solde.montant,
        description=f"Recharge via {recharge.reseau.upper()} - Ref: {recharge.reference_transaction}"
    )
    db.session.add(trx)
    notif = Notification(
        user_id=recharge.user_id,
        titre="Recharge validee !",
        message=f"Votre recharge de {recharge.montant:,.0f} FCFA a ete validee. Nouveau solde: {solde.montant:,.0f} FCFA",
        type_notif="success",
        lien=url_for("paiements.dashboard")
    )
    db.session.add(notif)
    db.session.commit()
    AuditLog.log(current_user.id, "recharge_validee", f"User: {recharge.user_id}, Montant: {recharge.montant}", ip=request.remote_addr)
    db.session.commit()
    flash(f"Recharge de {recharge.montant:,.0f} FCFA validee !", "success")
    return redirect(url_for("admin.gerer_recharges"))

@admin.route("/recharges/<int:recharge_id>/rejeter", methods=["POST"])
@admin_requis
def rejeter_recharge(recharge_id):
    from ..models import Recharge
    recharge = Recharge.query.get_or_404(recharge_id)
    note = request.form.get("note", "").strip()
    recharge.statut = "rejete"
    recharge.note_admin = note
    recharge.valide_par = current_user.id
    recharge.valide_le = datetime.utcnow()
    notif = Notification(
        user_id=recharge.user_id,
        titre="Recharge rejetee",
        message=f"Votre recharge de {recharge.montant:,.0f} FCFA a ete rejetee. Motif: {note}",
        type_notif="danger",
        lien=url_for("paiements.recharger")
    )
    db.session.add(notif)
    db.session.commit()
    flash("Recharge rejetee.", "warning")
    return redirect(url_for("admin.gerer_recharges"))

@admin.route("/soldes")
@admin_requis
def gerer_soldes():
    from ..models import Solde
    soldes = Solde.query.order_by(Solde.montant.desc()).all()
    total = sum(s.montant for s in soldes)
    return render_template("admin/soldes.html", soldes=soldes, total=total)
"""

content = content.rstrip() + nouvelles_routes
open("app/admin/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
