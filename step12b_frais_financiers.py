content = open("app/admin/__init__.py", encoding="utf-8-sig", errors="replace").read()

ancien = """    solde_avant = solde.montant
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
    db.session.add(trx)"""

nouveau = """    from ..models import FraisTransaction, FondsGarantie, MembreTontine
    montant_frais_total = round(recharge.montant * 0.015, 2)
    montant_fonds = round(recharge.montant * 0.005, 2)
    montant_ts = round(recharge.montant * 0.010, 2)
    montant_net = recharge.montant - montant_frais_total

    solde_avant = solde.montant
    solde.montant += montant_net
    recharge.statut = "valide"
    recharge.valide_par = current_user.id
    recharge.valide_le = datetime.utcnow()

    trx = Transaction(
        reference=Transaction.generer_reference(),
        user_id=recharge.user_id,
        type_transaction="recharge",
        montant=montant_net,
        sens="credit",
        solde_avant=solde_avant,
        solde_apres=solde.montant,
        description=f"Recharge via {recharge.reseau.upper()} — Montant net après frais 1,5 % — Réf : {recharge.reference_transaction}"
    )
    db.session.add(trx)

    frais = FraisTransaction(
        reference=FraisTransaction.generer_reference(),
        user_id=recharge.user_id,
        type_frais="recharge",
        montant_base=recharge.montant,
        taux=1.5,
        montant_frais=montant_frais_total,
        montant_fonds_garantie=montant_fonds,
        montant_tontinesecure=montant_ts,
        description=f"Frais 1,5 % — recharge {recharge.reference} — 0,5 % fonds garantie + 1 % TontineSecure"
    )
    db.session.add(frais)

    membership = MembreTontine.query.filter_by(user_id=recharge.user_id, statut="actif").first()
    if membership:
        fg = FondsGarantie.query.filter_by(tontine_id=membership.tontine_id).first()
        if fg:
            fg.montant += montant_fonds
            if not fg.actif and fg.montant >= fg.seuil_activation:
                fg.actif = True
                notif_fonds = Notification(
                    user_id=current_user.id,
                    titre="Fonds de garantie activé !",
                    message=f"Le fonds de garantie de la tontine {membership.tontine_id} a atteint son seuil — la garantie de paiement est désormais active.",
                    type_notif="success",
                    lien="/admin/tableau-de-bord"
                )
                db.session.add(notif_fonds)"""

if "montant_frais_total" not in content:
    content = content.replace(ancien, nouveau)
    open("app/admin/__init__.py", "w", encoding="utf-8").write(content)
    print("OK frais 1,5 % intégrés dans valider_recharge!")
else:
    print("Déjà intégré!")

# Scheduler frais annuels
scheduler_content = open("app/scheduler.py", encoding="utf-8-sig", errors="replace").read()

frais_annuels_job = """
def prelever_frais_annuels(app):
    with app.app_context():
        from .models import db, Solde, Transaction, Notification, MembreTontine, Tontine, FraisAnnuel
        from datetime import datetime
        logger.info("Début prélèvement frais annuels...")
        annee = datetime.utcnow().year
        membres = MembreTontine.query.filter_by(statut="actif").all()
        for m in membres:
            tontine = Tontine.query.get(m.tontine_id)
            if not tontine or tontine.statut != "en_cours":
                continue
            deja = FraisAnnuel.query.filter_by(user_id=m.user_id, tontine_id=tontine.id, annee=annee).first()
            if deja:
                continue
            montant_frais = round(tontine.montant_panier * 0.01, 2)
            solde = Solde.query.filter_by(user_id=m.user_id).first()
            frais = FraisAnnuel(
                reference=FraisAnnuel.generer_reference(),
                user_id=m.user_id,
                tontine_id=tontine.id,
                montant=montant_frais,
                annee=annee
            )
            db.session.add(frais)
            if solde and solde.montant >= montant_frais:
                solde_avant = solde.montant
                solde.montant -= montant_frais
                trx = Transaction(
                    reference=Transaction.generer_reference(),
                    user_id=m.user_id,
                    tontine_id=tontine.id,
                    type_transaction="frais_annuel",
                    montant=montant_frais,
                    sens="debit",
                    solde_avant=solde_avant,
                    solde_apres=solde.montant,
                    description=f"Frais annuels de tenue de compte {annee} — Tontine {tontine.code} — 1 % du panier"
                )
                db.session.add(trx)
                frais.statut = "preleve"
                frais.preleve_le = datetime.utcnow()
                notif = Notification(
                    user_id=m.user_id,
                    titre="Frais annuels prélevés",
                    message=f"Frais de tenue de compte {annee} : {montant_frais:,.0f} FCFA débités — Tontine {tontine.code}.",
                    type_notif="info",
                    lien="/paiements/"
                )
                db.session.add(notif)
            else:
                notif = Notification(
                    user_id=m.user_id,
                    titre="Frais annuels — Solde insuffisant",
                    message=f"Solde insuffisant pour les frais annuels {annee} ({montant_frais:,.0f} FCFA). Veuillez recharger.",
                    type_notif="warning",
                    lien="/paiements/recharger"
                )
                db.session.add(notif)
        db.session.commit()
        logger.info("Prélèvement frais annuels terminé.")
"""

if "prelever_frais_annuels" not in scheduler_content:
    scheduler_content = scheduler_content.replace(
        "def init_scheduler(app):",
        frais_annuels_job + "\ndef init_scheduler(app):"
    )
    scheduler_content = scheduler_content.replace(
        "    scheduler.start()\n    logger.info(\"Scheduler demarre - debit le 5, penalites le 9 de chaque mois\")",
        """    scheduler.add_job(
        func=prelever_frais_annuels,
        args=[app],
        trigger="cron",
        month=1,
        day=1,
        hour=1,
        minute=0,
        id="frais_annuels"
    )
    scheduler.start()
    logger.info("Scheduler démarré — débit le 5, pénalités le 9, frais annuels le 1er janvier")"""
    )
    open("app/scheduler.py", "w", encoding="utf-8").write(scheduler_content)
    print("OK frais annuels dans le scheduler!")
else:
    print("Déjà présent!")
