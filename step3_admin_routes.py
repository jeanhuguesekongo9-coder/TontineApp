texte = """
@admin.route("/penalites")
@admin_requis
def gerer_penalites():
    from ..models import Penalite, Utilisateur, Tontine
    statut = request.args.get("statut", "en_cours")
    penalites = Penalite.query.filter_by(statut=statut).order_by(Penalite.created_at.desc()).all()
    total_du = sum(p.montant_du + p.montant_penalite for p in penalites if p.statut == "en_cours")
    mises_en_demeure = Penalite.query.filter_by(statut="mise_en_demeure").count()
    return render_template("admin/penalites.html",
        penalites=penalites, statut=statut,
        total_du=total_du, mises_en_demeure=mises_en_demeure)

@admin.route("/penalites/<int:pen_id>/regulariser", methods=["POST"])
@admin_requis
def regulariser_penalite(pen_id):
    from ..models import Penalite, Solde, Transaction, MembreTontine
    pen = Penalite.query.get_or_404(pen_id)
    solde = Solde.query.filter_by(user_id=pen.user_id).first()
    montant_total = pen.montant_du + pen.montant_penalite
    if not solde or solde.montant < montant_total:
        flash(f"Solde insuffisant. Necessite {montant_total:,.0f} FCFA.", "danger")
        return redirect(url_for("admin.gerer_penalites"))
    solde_avant = solde.montant
    solde.montant -= montant_total
    trx = Transaction(
        reference=Transaction.generer_reference(),
        user_id=pen.user_id,
        tontine_id=pen.tontine_id,
        type_transaction="cotisation",
        montant=montant_total,
        sens="debit",
        solde_avant=solde_avant,
        solde_apres=solde.montant,
        description=f"Regularisation penalite {pen.reference} - cotisation {pen.mois_reference} + penalite 1.5%"
    )
    db.session.add(trx)
    pen.statut = "regularise"
    pen.regularise_le = datetime.utcnow()
    membre = MembreTontine.query.filter_by(user_id=pen.user_id, tontine_id=pen.tontine_id).first()
    if membre and membre.statut == "suspendu":
        autres_pen = Penalite.query.filter_by(user_id=pen.user_id, tontine_id=pen.tontine_id, statut="mise_en_demeure").count()
        if autres_pen == 0:
            membre.statut = "actif"
    notif = Notification(
        user_id=pen.user_id,
        titre="Penalite regularisee",
        message=f"Votre penalite de {pen.mois_reference} a ete regularisee. Montant debite: {montant_total:,.0f} FCFA (cotisation + 1.5%). Solde restant: {solde.montant:,.0f} FCFA",
        type_notif="success",
        lien="/paiements/"
    )
    db.session.add(notif)
    AuditLog.log(current_user.id, "penalite_regularisee", f"Penalite {pen.reference}, user {pen.user_id}", ip=request.remote_addr)
    db.session.commit()
    flash(f"Penalite regularisee ! {montant_total:,.0f} FCFA debites.", "success")
    return redirect(url_for("admin.gerer_penalites"))

@admin.route("/penalites/<int:pen_id>/annuler", methods=["POST"])
@admin_requis
def annuler_penalite(pen_id):
    from ..models import Penalite, MembreTontine
    pen = Penalite.query.get_or_404(pen_id)
    note = request.form.get("note", "Annulee par admin").strip()
    pen.statut = "annulee"
    pen.note_admin = note
    pen.regularise_le = datetime.utcnow()
    membre = MembreTontine.query.filter_by(user_id=pen.user_id, tontine_id=pen.tontine_id).first()
    if membre and membre.statut == "suspendu":
        membre.statut = "actif"
    notif = Notification(
        user_id=pen.user_id,
        titre="Penalite annulee",
        message=f"Votre penalite du mois {pen.mois_reference} a ete annulee par l administration. Motif: {note}",
        type_notif="success",
        lien="/paiements/"
    )
    db.session.add(notif)
    AuditLog.log(current_user.id, "penalite_annulee", f"Penalite {pen.reference}, motif: {note}", ip=request.remote_addr)
    db.session.commit()
    flash("Penalite annulee.", "warning")
    return redirect(url_for("admin.gerer_penalites"))

@admin.route("/tableau-de-bord")
@admin_requis
def tableau_de_bord():
    from ..models import Solde, Recharge, Transaction, Penalite, MembreTontine, Tontine, Utilisateur, KYC
    total_soldes = db.session.query(db.func.sum(Solde.montant)).scalar() or 0
    total_membres = Utilisateur.query.filter_by(role="membre").count()
    membres_actifs = MembreTontine.query.filter_by(statut="actif").count()
    membres_suspendus = MembreTontine.query.filter_by(statut="suspendu").count()
    recharges_attente = Recharge.query.filter_by(statut="en_attente").count()
    penalites_cours = Penalite.query.filter_by(statut="en_cours").count()
    mises_en_demeure = Penalite.query.filter_by(statut="mise_en_demeure").count()
    total_penalites_dues = db.session.query(db.func.sum(Penalite.montant_penalite)).filter(
        Penalite.statut.in_(["en_cours", "mise_en_demeure"])
    ).scalar() or 0
    total_cotisations = db.session.query(db.func.sum(Transaction.montant)).filter_by(
        type_transaction="cotisation", sens="debit"
    ).scalar() or 0
    tontines_actives = Tontine.query.filter_by(statut="en_cours").count()
    kyc_attente = KYC.query.filter_by(statut="en_attente").count()
    retardataires = db.session.query(
        Penalite.user_id,
        Utilisateur.email,
        db.func.count(Penalite.id).label("nb_impayes"),
        db.func.sum(Penalite.montant_du + Penalite.montant_penalite).label("total_du")
    ).join(Utilisateur, Penalite.user_id == Utilisateur.id).filter(
        Penalite.statut.in_(["en_cours", "mise_en_demeure"])
    ).group_by(Penalite.user_id, Utilisateur.email).order_by(
        db.func.count(Penalite.id).desc()
    ).limit(10).all()
    from ..models import Profil
    retardataires_detail = []
    for r in retardataires:
        profil = Profil.query.filter_by(user_id=r.user_id).first()
        retardataires_detail.append({
            "user_id": r.user_id,
            "nom": profil.nom_complet if profil else r.email,
            "email": r.email,
            "nb_impayes": r.nb_impayes,
            "total_du": r.total_du,
            "en_poursuite": r.nb_impayes >= 3
        })
    return render_template("admin/tableau_de_bord.html",
        total_soldes=total_soldes,
        total_membres=total_membres,
        membres_actifs=membres_actifs,
        membres_suspendus=membres_suspendus,
        recharges_attente=recharges_attente,
        penalites_cours=penalites_cours,
        mises_en_demeure=mises_en_demeure,
        total_penalites_dues=total_penalites_dues,
        total_cotisations=total_cotisations,
        tontines_actives=tontines_actives,
        kyc_attente=kyc_attente,
        retardataires=retardataires_detail
    )
"""
content = open("app/admin/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.rstrip() + texte
open("app/admin/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
