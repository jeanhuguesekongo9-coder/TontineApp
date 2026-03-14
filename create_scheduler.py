texte = """# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def debiter_cotisations_mensuelles(app):
    with app.app_context():
        from .models import db, Solde, Transaction, Notification, Participation, Tontine
        logger.info("Debut debit automatique cotisations...")
        participations = Participation.query.filter_by(statut="actif").all()
        for p in participations:
            tontine = Tontine.query.get(p.tontine_id)
            if not tontine:
                continue
            solde = Solde.query.filter_by(user_id=p.user_id).first()
            if not solde:
                solde = Solde(user_id=p.user_id, montant=0.0)
                db.session.add(solde)
                db.session.flush()
            if solde.montant >= tontine.montant_cotisation:
                solde_avant = solde.montant
                solde.montant -= tontine.montant_cotisation
                trx = Transaction(
                    reference=Transaction.generer_reference(),
                    user_id=p.user_id,
                    tontine_id=tontine.id,
                    type_transaction="cotisation",
                    montant=tontine.montant_cotisation,
                    sens="debit",
                    solde_avant=solde_avant,
                    solde_apres=solde.montant,
                    description=f"Cotisation mensuelle - Tontine: {tontine.nom}"
                )
                db.session.add(trx)
                notif = Notification(
                    user_id=p.user_id,
                    titre="Cotisation prelevee",
                    message=f"Votre cotisation de {tontine.montant_cotisation:,.0f} FCFA pour {tontine.nom} a ete prelevee. Solde restant: {solde.montant:,.0f} FCFA",
                    type_notif="info",
                    lien="/paiements/"
                )
                db.session.add(notif)
                logger.info(f"Cotisation prelevee: user {p.user_id}, tontine {tontine.id}")
            else:
                notif = Notification(
                    user_id=p.user_id,
                    titre="Solde insuffisant - ACTION REQUISE",
                    message=f"Votre solde est insuffisant pour la cotisation de {tontine.montant_cotisation:,.0f} FCFA (tontine: {tontine.nom}). Veuillez recharger dans les 48h.",
                    type_notif="danger",
                    lien="/paiements/recharger"
                )
                db.session.add(notif)
                logger.warning(f"Solde insuffisant: user {p.user_id}, tontine {tontine.id}")
        db.session.commit()
        logger.info("Debit automatique termine.")

def init_scheduler(app):
    scheduler = BackgroundScheduler(timezone="Africa/Abidjan")
    scheduler.add_job(
        func=debiter_cotisations_mensuelles,
        args=[app],
        trigger="cron",
        day=5,
        hour=0,
        minute=0,
        id="debit_cotisations"
    )
    scheduler.start()
    logger.info("Scheduler demarre - debit le 5 de chaque mois a minuit")
    return scheduler
"""
open("app/scheduler.py", "w", encoding="utf-8").write(texte)
print("OK!")
