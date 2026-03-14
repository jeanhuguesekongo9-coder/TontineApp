import os

# Route admin pour voir tous les contrats
admin_content = open("app/admin/__init__.py", encoding="utf-8-sig", errors="replace").read()

nouvelle_route_admin = """
@admin.route("/contrats")
@admin_requis
def gerer_contrats():
    from ..models import Contrat, Utilisateur, Profil
    statut = request.args.get("statut", "signes")
    if statut == "signes":
        contrats = Contrat.query.filter_by(signe=True).order_by(Contrat.signe_le.desc()).all()
    else:
        contrats = Contrat.query.filter_by(signe=False).order_by(Contrat.created_at.desc()).all()
    total_signes = Contrat.query.filter_by(signe=True).count()
    total_en_attente = Contrat.query.filter_by(signe=False).count()
    return render_template("admin/contrats.html",
        contrats=contrats,
        statut=statut,
        total_signes=total_signes,
        total_en_attente=total_en_attente
    )

@admin.route("/contrats/voir/<string:reference>")
@admin_requis
def voir_contrat_admin(reference):
    from ..models import Contrat
    contrat = Contrat.query.filter_by(reference=reference).first_or_404()
    if not contrat.contenu_html:
        flash("Ce contrat n'a pas encore de contenu archivé.", "warning")
        return redirect(url_for("admin.gerer_contrats"))
    return contrat.contenu_html, 200, {"Content-Type": "text/html; charset=utf-8"}
"""

admin_content = admin_content.rstrip() + nouvelle_route_admin
open("app/admin/__init__.py", "w", encoding="utf-8").write(admin_content)
print("OK routes admin contrats!")

# Template admin/contrats.html
os.makedirs("app/templates/admin", exist_ok=True)
contrats_admin_html = """{% extends "base.html" %}
{% block title %}Gestion des Contrats - Admin{% endblock %}
{% block content %}
<div class="fade-in">
  <h1 class="page-title">Gestion des Contrats</h1>
  <p class="page-subtitle">Tous les contrats signés par les membres — archivés et inaltérables</p>

  <!-- Stats -->
  <div class="row g-3 mb-4">
    <div class="col-md-4">
      <div class="card text-center p-3" style="border-left:4px solid #27ae60;">
        <div style="font-size:1.8rem;font-weight:700;color:#27ae60;">{{ total_signes }}</div>
        <small class="text-muted">Contrats signés et archivés</small>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card text-center p-3" style="border-left:4px solid #f0a500;">
        <div style="font-size:1.8rem;font-weight:700;color:#f0a500;">{{ total_en_attente }}</div>
        <small class="text-muted">En attente de signature</small>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card text-center p-3" style="border-left:4px solid #1a1a2e;">
        <div style="font-size:1.8rem;font-weight:700;color:#1a1a2e;">{{ total_signes + total_en_attente }}</div>
        <small class="text-muted">Total contrats émis</small>
      </div>
    </div>
  </div>

  <!-- Filtres -->
  <div class="mb-4 d-flex gap-2">
    <a href="?statut=signes" class="btn {% if statut == 'signes' %}btn-success{% else %}btn-outline-success{% endif %}">
      ✅ Signés ({{ total_signes }})
    </a>
    <a href="?statut=en_attente" class="btn {% if statut == 'en_attente' %}btn-warning{% else %}btn-outline-warning{% endif %}">
      ⏳ En attente ({{ total_en_attente }})
    </a>
  </div>

  <div class="card">
    <div class="card-body">
      {% if contrats %}
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead style="background:#f8f9fa;">
            <tr>
              <th>Référence</th>
              <th>Membre</th>
              <th>Email</th>
              <th>Tontine</th>
              <th>Cotisation</th>
              <th>Date signature</th>
              <th>IP signature</th>
              <th>Intégrité</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {% for c in contrats %}
            <tr>
              <td><code style="font-size:0.82rem;">{{ c.reference }}</code></td>
              <td>
                <strong>{{ c.utilisateur.profil.nom_complet if c.utilisateur.profil else '-' }}</strong>
              </td>
              <td><small style="color:#666;">{{ c.utilisateur.email }}</small></td>
              <td>
                <span class="badge" style="background:#1a1a2e;color:#f0a500;padding:5px 10px;">
                  {{ c.tontine.code }}
                </span>
              </td>
              <td><strong>{{ "{:,.0f}".format(c.tontine.montant_panier) }} FCFA</strong></td>
              <td>
                {% if c.signe_le %}
                <span style="font-size:0.85rem;">{{ c.signe_le.strftime('%d/%m/%Y') }}</span><br>
                <small style="color:#999;">{{ c.signe_le.strftime('%H:%M') }}</small>
                {% else %}
                <span style="color:#f0a500;">⏳ Non signé</span>
                {% endif %}
              </td>
              <td><small style="color:#666;">{{ c.ip_signature or '-' }}</small></td>
              <td>
                {% if c.hash_contrat %}
                <code style="font-size:0.72rem;color:#27ae60;">{{ c.hash_contrat[:12] }}...</code>
                {% else %}
                <span style="color:#ccc;">—</span>
                {% endif %}
              </td>
              <td>
                {% if c.signe and c.contenu_html %}
                <a href="{{ url_for('admin.voir_contrat_admin', reference=c.reference) }}"
                   target="_blank"
                   class="btn btn-sm btn-outline-dark">
                  👁️ Voir
                </a>
                {% else %}
                <span style="color:#ccc;font-size:0.82rem;">Non archivé</span>
                {% endif %}
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {% else %}
      <div class="text-center py-5">
        <div style="font-size:3rem;">📄</div>
        <p class="text-muted mt-2">Aucun contrat {{ 'signé' if statut == 'signes' else 'en attente' }} pour le moment.</p>
      </div>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}"""

open("app/templates/admin/contrats.html", "w", encoding="utf-8").write(contrats_admin_html)
print("OK admin/contrats.html!")

# Ajouter lien dans navbar admin
content = open("app/templates/base.html", encoding="utf-8-sig", errors="replace").read()
if "gerer_contrats" not in content:
    content = content.replace(
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.tableau_de_bord') }}">📊 Tableau de bord</a></li>""",
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.tableau_de_bord') }}">📊 Tableau de bord</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.gerer_contrats') }}">📄 Contrats</a></li>"""
    )
    open("app/templates/base.html", "w", encoding="utf-8").write(content)
    print("OK navbar admin contrats!")
