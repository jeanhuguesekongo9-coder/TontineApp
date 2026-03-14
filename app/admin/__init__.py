# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from ..models import db, Utilisateur, KYC, Tontine, Paiement, AuditLog, Notification, MembreTontine
import openpyxl
import io

admin = Blueprint("admin", __name__)

def admin_requis(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != "admin":
            flash("Acces reserve aux administrateurs.", "danger")
            return redirect(url_for("main.tableau_de_bord"))
        return f(*args, **kwargs)
    return decorated

@admin.route("/")
@admin_requis
def dashboard():
    stats = {
        "total_utilisateurs": Utilisateur.query.count(),
        "kyc_en_attente": KYC.query.filter_by(statut="en_attente").count(),
        "kyc_approuves": KYC.query.filter_by(statut="approuve").count(),
        "tontines_actives": Tontine.query.filter_by(statut="en_cours").count(),
        "tontines_recrut": Tontine.query.filter_by(statut="recrutement").count(),
        "paiements_en_attente": Paiement.query.filter_by(statut="en_attente").count(),
    }
    kycs_recents = KYC.query.filter_by(statut="en_attente").order_by(KYC.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", stats=stats, kycs_recents=kycs_recents)

@admin.route("/kyc")
@admin_requis
def gerer_kyc():
    statut_filtre = request.args.get("statut", "en_attente")
    kycs = KYC.query.filter_by(statut=statut_filtre).order_by(KYC.created_at).all()
    return render_template("admin/kyc.html", kycs=kycs, statut_filtre=statut_filtre)

@admin.route("/kyc/<int:kyc_id>/approuver", methods=["POST"])
@admin_requis
def approuver_kyc(kyc_id):
    kyc = KYC.query.get_or_404(kyc_id)
    kyc.statut = "approuve"
    kyc.verifie_par = current_user.id
    kyc.verifie_le = datetime.utcnow()
    kyc.utilisateur.kyc_valide = True
    notif = Notification(user_id=kyc.user_id,
        titre="Dossier approuve",
        message="Votre dossier KYC a ete approuve. Vous pouvez rejoindre une tontine !",
        type_notif="success",
        lien=url_for("tontines.liste"))
    db.session.add(notif)
    db.session.commit()
    AuditLog.log(current_user.id, "kyc_approuve", f"User: {kyc.user_id}", ip=request.remote_addr)
    db.session.commit()
    flash("KYC approuve.", "success")
    return redirect(url_for("admin.gerer_kyc"))

@admin.route("/kyc/<int:kyc_id>/rejeter", methods=["POST"])
@admin_requis
def rejeter_kyc(kyc_id):
    kyc = KYC.query.get_or_404(kyc_id)
    note = request.form.get("note", "").strip()
    kyc.statut = "rejete"
    kyc.note_admin = note
    kyc.verifie_par = current_user.id
    notif = Notification(user_id=kyc.user_id,
        titre="Dossier rejete",
        message=f"Votre dossier KYC a ete rejete. Motif : {note}.",
        type_notif="danger",
        lien=url_for("kyc.soumettre"))
    db.session.add(notif)
    db.session.commit()
    flash("KYC rejete.", "warning")
    return redirect(url_for("admin.gerer_kyc"))

@admin.route("/tontines")
@admin_requis
def gerer_tontines():
    tontines = Tontine.query.order_by(Tontine.created_at.desc()).all()
    return render_template("admin/tontines.html", tontines=tontines)

@admin.route("/tontines/creer", methods=["GET", "POST"])
@admin_requis
def creer_tontine():
    paniers = [50000, 100000, 200000]
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        montant = float(request.form.get("montant_panier", 0))
        min_m = int(request.form.get("min_membres", 5))
        max_m = int(request.form.get("max_membres", 10))
        jour = int(request.form.get("jour_collecte", 1))
        description = request.form.get("description", "")
        if not nom or montant not in paniers:
            flash("Donnees invalides.", "danger")
            return render_template("admin/creer_tontine.html", paniers=paniers)
        tontine = Tontine(code=Tontine.generer_code(), nom=nom,
            montant_panier=montant, min_membres=min_m, max_membres=max_m,
            jour_collecte=jour, description=description, createur_id=current_user.id)
        db.session.add(tontine)
        db.session.commit()
        flash(f"Tontine {tontine.nom} creee !", "success")
        return redirect(url_for("admin.gerer_tontines"))
    return render_template("admin/creer_tontine.html", paniers=paniers)

@admin.route("/tontines/<int:tontine_id>/demarrer", methods=["POST"])
@admin_requis
def demarrer_tontine(tontine_id):
    import random
    tontine = Tontine.query.get_or_404(tontine_id)
    if not tontine.peut_demarrer:
        flash("Pas assez de membres.", "warning")
        return redirect(url_for("admin.gerer_tontines"))
    tontine.statut = "en_cours"
    tontine.date_debut = datetime.utcnow()
    membres = tontine.membres.all()
    random.shuffle(membres)
    for i, m in enumerate(membres, 1):
        m.ordre_collecte = i
    db.session.commit()
    flash(f"Tontine {tontine.nom} demarree !", "success")
    return redirect(url_for("admin.gerer_tontines"))

@admin.route("/utilisateurs")
@admin_requis
def utilisateurs():
    users = Utilisateur.query.order_by(Utilisateur.created_at.desc()).all()
    return render_template("admin/utilisateurs.html", users=users)

@admin.route("/logs")
@admin_requis
def logs():
    page = request.args.get("page", 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=50)
    return render_template("admin/logs.html", logs=logs)

@admin.route("/export-excel")
@admin_requis
def export_excel():
    wb = openpyxl.Workbook()
    header_fill = openpyxl.styles.PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = openpyxl.styles.Font(bold=True, color="FFFFFF")

    def style_headers(ws, headers):
        ws.append(headers)
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font

    # Onglet Utilisateurs
    ws1 = wb.active
    ws1.title = "Utilisateurs"
    style_headers(ws1, ["ID", "Email", "Role", "Email verifie", "KYC valide", "Compte actif", "Date inscription"])
    for u in Utilisateur.query.order_by(Utilisateur.created_at.desc()).all():
        ws1.append([u.id, u.email, u.role, u.email_verifie, u.kyc_valide, u.compte_actif, str(u.created_at)[:19]])

    # Onglet Profils
    ws2 = wb.create_sheet("Profils")
    style_headers(ws2, ["ID", "User ID", "Nom", "Prenom", "Telephone", "Ville", "Pays", "Profession"])
    from ..models import Profil
    for p in Profil.query.all():
        ws2.append([p.id, p.user_id, p.nom, p.prenom, p.telephone, p.ville or "", p.pays or "", p.profession or ""])

    # Onglet KYC
    ws3 = wb.create_sheet("KYC")
    style_headers(ws3, ["ID", "User ID", "Type doc", "Statut", "Note admin", "Date soumission"])
    for k in KYC.query.order_by(KYC.created_at.desc()).all():
        ws3.append([k.id, k.user_id, k.type_doc or "", k.statut, k.note_admin or "", str(k.created_at)[:19]])

    # Onglet Tontines
    ws4 = wb.create_sheet("Tontines")
    style_headers(ws4, ["ID", "Code", "Nom", "Montant panier", "Min membres", "Max membres", "Nb membres", "Statut", "Date creation"])
    for t in Tontine.query.order_by(Tontine.created_at.desc()).all():
        ws4.append([t.id, t.code, t.nom, t.montant_panier, t.min_membres, t.max_membres, t.nombre_membres, t.statut, str(t.created_at)[:19]])

    # Onglet Membres Tontines
    ws5 = wb.create_sheet("Membres Tontines")
    style_headers(ws5, ["ID", "User ID", "Tontine ID", "Ordre collecte", "A recu", "Statut", "Date adhesion"])
    for m in MembreTontine.query.all():
        ws5.append([m.id, m.user_id, m.tontine_id, m.ordre_collecte or "", m.a_recu, m.statut, str(m.date_adhesion)[:19]])

    # Onglet Paiements
    ws6 = wb.create_sheet("Paiements")
    style_headers(ws6, ["ID", "Reference", "User ID", "Tontine ID", "Montant", "Type", "Statut", "Date"])
    for p in Paiement.query.order_by(Paiement.created_at.desc()).all():
        ws6.append([p.id, p.reference, p.user_id, p.tontine_id, p.montant, p.type_paiement or "", p.statut, str(p.created_at)[:19]])

    # Ajuster largeurs
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = max((len(str(cell.value)) for cell in col if cell.value), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"tontinesecure_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.xlsx"
    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@admin.route("/fichier/<path:chemin>")
@admin_requis
def voir_fichier(chemin):
    import os
    from supabase import create_client
    from flask import redirect
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(url, key)
    result = client.storage.from_("kyc-documents").create_signed_url(chemin, 300)
    return redirect(result["signedURL"])
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
