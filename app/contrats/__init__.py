from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, current_app
from flask_login import login_required, current_user
from datetime import datetime
import os, hashlib
from ..models import db, Contrat, MembreTontine, AuditLog

contrats = Blueprint("contrats", __name__)

def generer_contrat_pdf(utilisateur, tontine):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    import secrets
    ref = Contrat.generer_reference()
    nom_fichier = f"contrat_{ref}.pdf"
    dossier = os.path.join(current_app.config["UPLOAD_FOLDER"], "contrats")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)
    doc = SimpleDocTemplate(chemin, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    or_ = HexColor("#f0a500")
    bleu = HexColor("#1a1a2e")
    gris = HexColor("#555555")
    titre_s = ParagraphStyle("t", fontSize=20, textColor=bleu, alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=6)
    sous_s = ParagraphStyle("s", fontSize=12, textColor=or_, alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=16)
    body_s = ParagraphStyle("b", fontSize=10, textColor=gris, fontName="Helvetica", spaceAfter=8, leading=16, alignment=TA_JUSTIFY)
    clause_s = ParagraphStyle("c", fontSize=10, textColor=bleu, fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=10)
    profil = utilisateur.profil
    c = []
    c.append(Paragraph("TONTINESECURE", titre_s))
    c.append(Paragraph("CONTRAT D ADHESION ET DE PARTICIPATION", sous_s))
    c.append(HRFlowable(width="100%", thickness=2, color=or_))
    c.append(Spacer(1, 0.4*cm))
    data = [["Reference:", ref], ["Date:", datetime.now().strftime("%d/%m/%Y %H:%M")],
            ["Tontine:", f"{tontine.nom} ({tontine.code})"],
            ["Montant mensuel:", f"{tontine.montant_panier:,.0f} FCFA"]]
    t = Table(data, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("TEXTCOLOR", (0,0), (0,-1), bleu),
        ("GRID", (0,0), (-1,-1), 0.5, HexColor("#dee2e6")),
        ("PADDING", (0,0), (-1,-1), 8),
    ]))
    c.append(t)
    c.append(Spacer(1, 0.4*cm))
    c.append(Paragraph("ARTICLE 1 - PARTIES CONTRACTANTES", clause_s))
    c.append(Paragraph(f"<b>L Adherent :</b> {profil.nom_complet}, ne(e) le {profil.date_naissance.strftime('%d/%m/%Y')}, residant a {profil.ville}, {profil.pays}. Telephone : {profil.telephone}.", body_s))
    c.append(Paragraph("<b>La Plateforme :</b> TontineSecure, plateforme de gestion de tontines securisees.", body_s))
    c.append(Paragraph("ARTICLE 2 - OBJET", clause_s))
    c.append(Paragraph(f"Adhesion a la tontine <b>{tontine.nom}</b> avec une cotisation mensuelle de <b>{tontine.montant_panier:,.0f} FCFA</b>.", body_s))
    c.append(Paragraph("ARTICLE 3 - ENGAGEMENTS", clause_s))
    for i, eng in enumerate(["Verser la cotisation avant le jour fixe chaque mois.",
        "Maintenir son adhesion pour toute la duree du cycle.",
        "Fournir des informations exactes et authentiques.",
        "Respecter la confidentialite des autres membres."], 1):
        c.append(Paragraph(f"{i}. {eng}", body_s))
    c.append(Paragraph("ARTICLE 4 - PENALITES", clause_s))
    c.append(Paragraph(f"Tout retard de plus de 5 jours entraine une penalite de 5% ({tontine.montant_panier*0.05:,.0f} FCFA). Au-dela de 15 jours : 10% et suspension possible.", body_s))
    c.append(Paragraph("ARTICLE 5 - REDISTRIBUTION", clause_s))
    c.append(Paragraph("L ordre de redistribution est determine par tirage au sort. Les fonds sont vires sur le RIB enregistre sous 48h ouvrees.", body_s))
    c.append(Spacer(1, 0.8*cm))
    c.append(HRFlowable(width="100%", thickness=1, color=HexColor("#dee2e6")))
    c.append(Spacer(1, 0.3*cm))
    c.append(Paragraph(f"Fait le {datetime.now().strftime('%d/%m/%Y')} - Signature electronique requise sur la plateforme.", body_s))
    doc.build(c)
    with open(chemin, "rb") as f:
        hash_pdf = hashlib.sha256(f.read()).hexdigest()
    contrat = Contrat(reference=ref, user_id=utilisateur.id, tontine_id=tontine.id,
        fichier_pdf=os.path.join("contrats", nom_fichier), hash_contrat=hash_pdf)
    db.session.add(contrat)
    return contrat

@contrats.route("/mes-contrats")
@login_required
def mes_contrats():
    mes = Contrat.query.filter_by(user_id=current_user.id).order_by(Contrat.created_at.desc()).all()
    return render_template("contrats/mes_contrats.html", contrats=mes)

@contrats.route("/signer/<int:contrat_id>", methods=["GET", "POST"])
@login_required
def signer(contrat_id):
    contrat = Contrat.query.get_or_404(contrat_id)
    if contrat.user_id != current_user.id:
        flash("Acces refuse.", "danger")
        return redirect(url_for("contrats.mes_contrats"))
    if contrat.signe:
        flash("Contrat deja signe.", "info")
        return redirect(url_for("contrats.mes_contrats"))
    if request.method == "POST":
        if not request.form.get("confirmation"):
            flash("Vous devez confirmer avoir lu le contrat.", "danger")
            return render_template("contrats/signer.html", contrat=contrat)
        import json
        contrat.signe = True
        contrat.signe_le = datetime.utcnow()
        contrat.ip_signature = request.remote_addr
        membership = MembreTontine.query.filter_by(user_id=current_user.id, tontine_id=contrat.tontine_id).first()
        if membership:
            membership.contrat_signe = True
            membership.contrat_signe_le = datetime.utcnow()
        db.session.commit()
        AuditLog.log(current_user.id, "contrat_signe", f"Ref: {contrat.reference}", ip=request.remote_addr)
        db.session.commit()
        flash(f"Contrat {contrat.reference} signe !", "success")
        return redirect(url_for("tontines.mes_tontines"))
    return render_template("contrats/signer.html", contrat=contrat)

@contrats.route("/telecharger/<int:contrat_id>")
@login_required
def telecharger(contrat_id):
    contrat = Contrat.query.get_or_404(contrat_id)
    if contrat.user_id != current_user.id:
        flash("Acces refuse.", "danger")
        return redirect(url_for("contrats.mes_contrats"))
    chemin = os.path.join(current_app.config["UPLOAD_FOLDER"], contrat.fichier_pdf)
    if not os.path.exists(chemin):
        flash("Fichier introuvable.", "danger")
        return redirect(url_for("contrats.mes_contrats"))
    return send_file(chemin, as_attachment=True, download_name=f"contrat_{contrat.reference}.pdf")
