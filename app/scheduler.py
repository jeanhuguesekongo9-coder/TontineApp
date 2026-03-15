# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def debiter_cotisations_mensuelles(app):
    with app.app_context():
        from .models import db, Solde, Transaction, Notification, MembreTontine, Tontine, Penalite
        logger.info("Debut debit automatique cotisations le 5...")
        membres = MembreTontine.query.filter_by(statut="actif").all()
        for m in membres:
            tontine = Tontine.query.get(m.tontine_id)
            if not tontine or tontine.statut != "en_cours":
                continue
            solde = Solde.query.filter_by(user_id=m.user_id).first()
            if not solde:
                solde = Solde(user_id=m.user_id, montant=0.0)
                db.session.add(solde)
                db.session.flush()
            mois_ref = datetime.utcnow().strftime("%Y-%m")
            if solde.montant >= tontine.montant_panier:
                solde_avant = solde.montant
                solde.montant -= tontine.montant_panier
                trx = Transaction(
                    reference=Transaction.generer_reference(),
                    user_id=m.user_id,
                    tontine_id=tontine.id,
                    type_transaction="cotisation",
                    montant=tontine.montant_panier,
                    sens="debit",
                    solde_avant=solde_avant,
                    solde_apres=solde.montant,
                    description=f"Cotisation mensuelle - Tontine {tontine.code} - {mois_ref}"
                )
                db.session.add(trx)
                notif = Notification(
                    user_id=m.user_id,
                    titre="Cotisation prelevee",
                    message=f"Votre cotisation de {tontine.montant_panier:,.0f} FCFA a ete prelevee automatiquement. Solde restant: {solde.montant:,.0f} FCFA",
                    type_notif="info",
                    lien="/paiements/"
                )
                db.session.add(notif)
                logger.info(f"Cotisation OK: user {m.user_id}, tontine {tontine.id}")
            else:
                notif = Notification(
                    user_id=m.user_id,
                    titre="URGENT - Solde insuffisant",
                    message=f"Votre solde est insuffisant pour la cotisation de {tontine.montant_panier:,.0f} FCFA. Vous avez jusqu au 9 pour recharger. Passe cette date, une penalite de 1.5% sera appliquee.",
                    type_notif="danger",
                    lien="/paiements/recharger"
                )
                db.session.add(notif)
                logger.warning(f"Solde insuffisant le 5: user {m.user_id}, tontine {tontine.id}")
        db.session.commit()
        logger.info("Debit automatique du 5 termine.")

def appliquer_penalites(app):
    with app.app_context():
        from .models import db, Solde, Transaction, Notification, MembreTontine, Tontine, Penalite
        logger.info("Debut application penalites le 9...")
        membres = MembreTontine.query.filter_by(statut="actif").all()
        mois_ref = datetime.utcnow().strftime("%Y-%m")
        for m in membres:
            tontine = Tontine.query.get(m.tontine_id)
            if not tontine or tontine.statut != "en_cours":
                continue
            cotisation_payee = Transaction.query.filter_by(
                user_id=m.user_id,
                tontine_id=tontine.id,
                type_transaction="cotisation",
                sens="debit"
            ).filter(
                Transaction.description.contains(mois_ref)
            ).first()
            if cotisation_payee:
                continue
            penalite_existante = Penalite.query.filter_by(
                user_id=m.user_id,
                tontine_id=tontine.id,
                mois_reference=mois_ref
            ).first()
            if penalite_existante:
                continue
            mois_impayes_total = Penalite.query.filter_by(
                user_id=m.user_id,
                tontine_id=tontine.id,
                statut="en_cours"
            ).count() + 1
            montant_penalite = round(tontine.montant_panier * 0.015, 2)
            penalite = Penalite(
                reference=Penalite.generer_reference(),
                user_id=m.user_id,
                tontine_id=tontine.id,
                montant_du=tontine.montant_panier,
                montant_penalite=montant_penalite,
                taux=1.5,
                mois_reference=mois_ref,
                statut="en_cours",
                mois_impaye=mois_impayes_total
            )
            db.session.add(penalite)
            message_base = f"Une penalite de {montant_penalite:,.0f} FCFA (1.5%) a ete appliquee pour retard de cotisation du mois {mois_ref}."
            if mois_impayes_total >= 3:
                penalite.statut = "mise_en_demeure"
                message_extra = " ATTENTION: 3 mois d impaye - Des poursuites judiciaires peuvent etre engagees conformement a votre contrat."
                m.statut = "suspendu"
            else:
                message_extra = f" Mois impaye: {mois_impayes_total}/3. Regularisez rapidement."
            notif = Notification(
                user_id=m.user_id,
                titre="Penalite appliquee - Retard de cotisation",
                message=message_base + message_extra,
                type_notif="danger",
                lien="/paiements/recharger"
            )
            db.session.add(notif)
            logger.warning(f"Penalite appliquee: user {m.user_id}, tontine {tontine.id}, mois {mois_ref}, nb impayes: {mois_impayes_total}")
        db.session.commit()
        logger.info("Application penalites du 9 terminee.")


def prelever_frais_annuels(app):
    with app.app_context():
        from .models import db, Solde, Transaction, Notification, MembreTontine, Tontine, FraisAnnuel
        from datetime import datetime
        logger.info("Début prélèvement frais annuels de tenue de compte...")
        annee = datetime.utcnow().year
        membres = MembreTontine.query.filter_by(statut="actif").all()
        for m in membres:
            tontine = Tontine.query.get(m.tontine_id)
            if not tontine or tontine.statut != "en_cours":
                continue
            deja = FraisAnnuel.query.filter_by(
                user_id=m.user_id,
                tontine_id=tontine.id,
                annee=annee
            ).first()
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
                    message=f"Les frais annuels de tenue de compte {annee} de {montant_frais:,.0f} FCFA ont été prélevés (1 % du panier — tontine {tontine.code}).",
                    type_notif="info",
                    lien="/paiements/"
                )
                db.session.add(notif)
            else:
                notif = Notification(
                    user_id=m.user_id,
                    titre="Frais annuels — Solde insuffisant",
                    message=f"Votre solde est insuffisant pour les frais annuels de tenue de compte {annee} ({montant_frais:,.0f} FCFA). Veuillez recharger.",
                    type_notif="warning",
                    lien="/paiements/recharger"
                )
                db.session.add(notif)
            logger.info(f"Frais annuel: user {m.user_id}, tontine {tontine.id}, montant {montant_frais}")
        db.session.commit()
        logger.info("Prélèvement frais annuels terminé.")

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
    scheduler.add_job(
        func=appliquer_penalites,
        args=[app],
        trigger="cron",
        day=9,
        hour=0,
        minute=1,
        id="penalites_retard"
    )
    scheduler.add_job(
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
    logger.info("Scheduler démarré — débit le 5, pénalités le 9, frais annuels le 1er janvier")
    return scheduler
