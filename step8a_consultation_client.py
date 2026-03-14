import os

# Route pour voir son contrat archive + telecharger en PDF
content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()

nouvelles_routes = """
@contrats.route("/voir/<string:reference>")
@login_required
def voir_contrat_archive(reference):
    from ..models import Contrat
    contrat = Contrat.query.filter_by(
        reference=reference,
        user_id=current_user.id
    ).first_or_404()
    if not contrat.contenu_html:
        flash("Le contenu archivé de ce contrat n'est pas encore disponible.", "warning")
        return redirect(url_for("contrats.mes_contrats"))
    return contrat.contenu_html, 200, {"Content-Type": "text/html; charset=utf-8"}

@contrats.route("/telecharger/<string:reference>")
@login_required
def telecharger_contrat(reference):
    from ..models import Contrat
    from flask import Response
    contrat = Contrat.query.filter_by(
        reference=reference,
        user_id=current_user.id
    ).first_or_404()
    if not contrat.contenu_html:
        flash("Le contenu archivé de ce contrat n'est pas encore disponible.", "warning")
        return redirect(url_for("contrats.mes_contrats"))
    html_avec_print = contrat.contenu_html.replace(
        "</head>",
        \"\"\"<style>
          @media print {
            body { margin: 20mm; }
            .no-print { display: none !important; }
          }
        </style>
        <script>window.onload = function() { window.print(); }</script>
        </head>\"\"\"
    )
    return Response(
        html_avec_print,
        mimetype="text/html",
        headers={
            "Content-Disposition": f"inline; filename=Contrat_{reference}.html",
            "Content-Type": "text/html; charset=utf-8"
        }
    )
"""

content = content.rstrip() + nouvelles_routes
open("app/contrats/__init__.py", "w", encoding="utf-8").write(content)
print("OK routes consultation et téléchargement!")

# Mettre a jour mes_contrats.html avec boutons voir + telecharger
mes_contrats_html = """{% extends "base.html" %}
{% block title %}Mes Contrats - TontineSecure{% endblock %}
{% block content %}
<div style="max-width:800px;margin:0 auto;" class="fade-in">
  <h1 class="page-title">Mes Contrats</h1>
  <p class="page-subtitle">Vos engagements contractuels archivés et sécurisés</p>

  {% if contrats %}
  {% for c in contrats %}
  <div class="card mb-3" style="border-radius:16px;overflow:hidden;">

    <!-- Bandeau statut -->
    {% if c.signe %}
    <div style="background:linear-gradient(90deg,#27ae60,#2ecc71);padding:8px 20px;display:flex;justify-content:space-between;align-items:center;">
      <span style="color:#fff;font-size:0.82rem;font-weight:600;">✅ CONTRAT SIGNÉ ET ARCHIVÉ</span>
      <span style="color:#fff;font-size:0.78rem;">{{ c.signe_le.strftime('%d/%m/%Y à %H:%M') }}</span>
    </div>
    {% else %}
    <div style="background:linear-gradient(90deg,#f0a500,#f39c12);padding:8px 20px;">
      <span style="color:#fff;font-size:0.82rem;font-weight:600;">⏳ EN ATTENTE DE SIGNATURE</span>
    </div>
    {% endif %}

    <div class="card-body p-4">
      <div class="row g-3 align-items-center">

        <!-- Infos contrat -->
        <div class="col-md-7">
          <div style="font-size:0.75rem;color:#888;font-weight:600;letter-spacing:1px;">RÉFÉRENCE</div>
          <div style="font-weight:700;color:#1a1a2e;font-size:1.15rem;margin-bottom:6px;">{{ c.reference }}</div>
          <div style="font-size:0.85rem;color:#555;">
            <span style="margin-right:15px;">🏦 Tontine : <strong>{{ c.tontine.code }}</strong></span>
            <span>💰 <strong>{{ "{:,.0f}".format(c.tontine.montant_panier) }} FCFA/mois</strong></span>
          </div>
          {% if c.signe %}
          <div style="font-size:0.78rem;color:#999;margin-top:6px;">
            🔐 Hash d'intégrité : <code>{{ c.hash_contrat[:20] if c.hash_contrat else '-' }}...</code>
          </div>
          <div style="font-size:0.78rem;color:#999;">
            📍 Signé depuis IP : {{ c.ip_signature }}
          </div>
          {% endif %}
        </div>

        <!-- Boutons actions -->
        <div class="col-md-5">
          {% if c.signe and c.contenu_html %}
          <div class="d-flex flex-column gap-2">
            <a href="{{ url_for('contrats.voir_contrat_archive', reference=c.reference) }}"
               target="_blank"
               style="display:flex;align-items:center;justify-content:center;gap:8px;
                      background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;
                      padding:10px 15px;border-radius:10px;text-decoration:none;
                      font-weight:600;font-size:0.88rem;transition:all 0.2s;">
              👁️ Consulter mon contrat
            </a>
            <a href="{{ url_for('contrats.telecharger_contrat', reference=c.reference) }}"
               target="_blank"
               style="display:flex;align-items:center;justify-content:center;gap:8px;
                      background:linear-gradient(135deg,#f0a500,#e67e22);color:#fff;
                      padding:10px 15px;border-radius:10px;text-decoration:none;
                      font-weight:600;font-size:0.88rem;">
              📥 Télécharger en PDF
            </a>
          </div>
          {% elif c.signe and not c.contenu_html %}
          <div style="text-align:center;color:#999;font-size:0.85rem;padding:10px;">
            📄 Contrat signé<br>
            <small>(archivage en cours de migration)</small>
          </div>
          {% else %}
          <a href="{{ url_for('contrats.voir_contrat', tontine_id=c.tontine_id) }}"
             style="display:flex;align-items:center;justify-content:center;gap:8px;
                    background:#f0a500;color:#fff;padding:10px 15px;border-radius:10px;
                    text-decoration:none;font-weight:600;font-size:0.88rem;">
            ✍️ Signer maintenant
          </a>
          {% endif %}
        </div>

      </div>
    </div>
  </div>
  {% endfor %}

  <!-- Bloc explication archivage -->
  <div style="background:#f0f8ff;border:1px solid #1DC8EE;border-radius:12px;padding:16px 20px;margin-top:10px;">
    <div style="font-weight:700;color:#1a1a2e;margin-bottom:6px;">🔐 Sécurité de vos contrats</div>
    <p style="color:#555;font-size:0.88rem;margin:0;line-height:1.7;">
      Tous vos contrats signés sont archivés de façon permanente et inaltérable dans nos bases de données.
      Ils sont horodatés, associés à votre adresse IP de signature, et dotés d'un hash d'intégrité unique.
      Vous pouvez les consulter ou les télécharger à tout moment.
    </p>
  </div>

  {% else %}
  <div class="card text-center p-5">
    <div style="font-size:3rem;">📄</div>
    <h5 style="color:#1a1a2e;margin-top:15px;">Aucun contrat pour le moment</h5>
    <p class="text-muted">Rejoignez une tontine pour signer votre premier contrat.</p>
  </div>
  {% endif %}
</div>
{% endblock %}"""

open("app/templates/contrats/mes_contrats.html", "w", encoding="utf-8").write(mes_contrats_html)
print("OK mes_contrats.html mis à jour!")
