import os
os.makedirs("app/templates/contrats", exist_ok=True)

texte = """# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
import secrets

contrats = Blueprint("contrats", __name__)

@contrats.route("/signer/<int:tontine_id>", methods=["GET"])
@login_required
def voir_contrat(tontine_id):
    from ..models import Tontine, Contrat, Profil
    tontine = Tontine.query.get_or_404(tontine_id)
    profil = Profil.query.filter_by(user_id=current_user.id).first()
    membre_nom = profil.nom_complet if profil else current_user.email
    contrat_existant = Contrat.query.filter_by(
        user_id=current_user.id,
        tontine_id=tontine_id
    ).first()
    deja_signe = contrat_existant and contrat_existant.signe
    reference_contrat = contrat_existant.reference if contrat_existant else "CTR-" + secrets.token_hex(6).upper()
    return render_template("contrats/contrat.html",
        tontine=tontine,
        membre_nom=membre_nom,
        membre_email=current_user.email,
        date_emission=datetime.utcnow().strftime("%d/%m/%Y"),
        reference_contrat=reference_contrat,
        deja_signe=deja_signe,
        contrat=contrat_existant
    )

@contrats.route("/signer/<int:tontine_id>", methods=["POST"])
@login_required
def signer_contrat(tontine_id):
    from ..models import db, Tontine, Contrat, MembreTontine, Notification, AuditLog, Profil
    tontine = Tontine.query.get_or_404(tontine_id)
    contrat_existant = Contrat.query.filter_by(
        user_id=current_user.id,
        tontine_id=tontine_id
    ).first()
    if contrat_existant and contrat_existant.signe:
        flash("Vous avez déjà signé ce contrat.", "info")
        return redirect(url_for("paiements.ma_tontine"))
    if not contrat_existant:
        contrat_existant = Contrat(
            reference="CTR-" + secrets.token_hex(6).upper(),
            user_id=current_user.id,
            tontine_id=tontine_id
        )
        db.session.add(contrat_existant)
        db.session.flush()
    contrat_existant.signe = True
    contrat_existant.signe_le = datetime.utcnow()
    contrat_existant.ip_signature = request.remote_addr
    contrat_existant.hash_contrat = secrets.token_hex(32)
    membre = MembreTontine.query.filter_by(
        user_id=current_user.id,
        tontine_id=tontine_id
    ).first()
    if not membre:
        nb_membres = MembreTontine.query.filter_by(tontine_id=tontine_id, statut="actif").count()
        membre = MembreTontine(
            user_id=current_user.id,
            tontine_id=tontine_id,
            ordre_collecte=nb_membres + 1,
            statut="actif",
            contrat_signe=True,
            contrat_signe_le=datetime.utcnow()
        )
        db.session.add(membre)
        tontine.nombre_membres = nb_membres + 1
    else:
        membre.contrat_signe = True
        membre.contrat_signe_le = datetime.utcnow()
    profil = Profil.query.filter_by(user_id=current_user.id).first()
    notif = Notification(
        user_id=current_user.id,
        titre="Contrat signé — Bienvenue dans la tontine !",
        message=f"Votre contrat de participation à la tontine {tontine.code} a été signé avec succès. Vous êtes officiellement membre. Référence : {contrat_existant.reference}",
        type_notif="success",
        lien=url_for("paiements.ma_tontine")
    )
    db.session.add(notif)
    AuditLog.log(
        current_user.id,
        "contrat_signe",
        f"Tontine {tontine.code}, réf. contrat {contrat_existant.reference}, IP : {request.remote_addr}"
    )
    db.session.commit()
    flash(f"Contrat signé avec succès ! Bienvenue dans la tontine {tontine.code}. Référence : {contrat_existant.reference}", "success")
    return redirect(url_for("paiements.ma_tontine"))

@contrats.route("/mes-contrats")
@login_required
def mes_contrats():
    from ..models import Contrat
    contrats_liste = Contrat.query.filter_by(user_id=current_user.id).order_by(Contrat.created_at.desc()).all()
    return render_template("contrats/mes_contrats.html", contrats=contrats_liste)
"""
open("app/contrats/__init__.py", "w", encoding="utf-8").write(texte)
print("OK routes contrats!")

mes_contrats_html = """{% extends "base.html" %}
{% block title %}Mes Contrats - TontineSecure{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;" class="fade-in">
  <h1 class="page-title">Mes Contrats</h1>
  <p class="page-subtitle">Historique de vos engagements contractuels</p>
  {% if contrats %}
  {% for c in contrats %}
  <div class="card mb-3" style="border-radius:16px;">
    <div class="card-body p-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <div style="font-size:0.78rem;color:#888;font-weight:600;">RÉFÉRENCE</div>
          <div style="font-weight:700;color:#1a1a2e;font-size:1.1rem;">{{ c.reference }}</div>
          <div style="font-size:0.85rem;color:#666;margin-top:4px;">
            Tontine : <strong>{{ c.tontine.code }}</strong> —
            Cotisation : <strong>{{ "{:,.0f}".format(c.tontine.montant_panier) }} FCFA/mois</strong>
          </div>
        </div>
        <div style="text-align:right;">
          {% if c.signe %}
          <span style="background:#27ae60;color:#fff;padding:6px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;">
            ✅ Signé le {{ c.signe_le.strftime('%d/%m/%Y') }}
          </span>
          {% else %}
          <a href="{{ url_for('contrats.voir_contrat', tontine_id=c.tontine_id) }}"
             style="background:#f0a500;color:#fff;padding:6px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;text-decoration:none;">
            ✍️ Signer maintenant
          </a>
          {% endif %}
        </div>
      </div>
      {% if c.signe %}
      <div style="margin-top:12px;font-size:0.78rem;color:#999;">
        Signé depuis IP : {{ c.ip_signature }} — Hash : {{ c.hash_contrat[:16] }}...
      </div>
      {% endif %}
    </div>
  </div>
  {% endfor %}
  {% else %}
  <div class="card text-center p-5">
    <div style="font-size:3rem;">📄</div>
    <p class="text-muted mt-2">Aucun contrat pour le moment.</p>
  </div>
  {% endif %}
</div>
{% endblock %}"""
open("app/templates/contrats/mes_contrats.html", "w", encoding="utf-8").write(mes_contrats_html)
print("OK mes_contrats.html!")

content = open("app/templates/base.html", encoding="utf-8-sig", errors="replace").read()
if "mes-contrats" not in content:
    content = content.replace(
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('paiements.ma_tontine') }}">🔒 Ma Tontine</a></li>""",
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('paiements.ma_tontine') }}">🔒 Ma Tontine</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('contrats.mes_contrats') }}">📄 Mes Contrats</a></li>"""
    )
    open("app/templates/base.html", "w", encoding="utf-8").write(content)
    print("OK navbar contrats!")
