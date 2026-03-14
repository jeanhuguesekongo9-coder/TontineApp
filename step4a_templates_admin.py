import os
os.makedirs("app/templates/admin", exist_ok=True)

# Template penalites.html
penalites_html = """{% extends "base.html" %}
{% block title %}Gestion des Penalites - Admin{% endblock %}
{% block content %}
<div class="fade-in">
  <h1 class="page-title">Gestion des Penalites</h1>
  <p class="page-subtitle">Retards de cotisation et mises en demeure</p>

  <!-- Stats rapides -->
  <div class="row g-3 mb-4">
    <div class="col-md-4">
      <div class="card text-center p-3" style="border-left:4px solid #e74c3c;">
        <div style="font-size:1.8rem;font-weight:700;color:#e74c3c;">{{ mises_en_demeure }}</div>
        <small class="text-muted">Mises en demeure (3+ mois)</small>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card text-center p-3" style="border-left:4px solid #f0a500;">
        <div style="font-size:1.8rem;font-weight:700;color:#f0a500;">{{ "{:,.0f}".format(total_du) }}</div>
        <small class="text-muted">FCFA total du (cotisations + penalites)</small>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card text-center p-3" style="border-left:4px solid #1a1a2e;">
        <div style="font-size:1.8rem;font-weight:700;color:#1a1a2e;">{{ penalites|length }}</div>
        <small class="text-muted">Penalites {{ statut.replace("_", " ") }}</small>
      </div>
    </div>
  </div>

  <!-- Filtres -->
  <div class="mb-4 d-flex gap-2 flex-wrap">
    <a href="?statut=en_cours" class="btn {% if statut == 'en_cours' %}btn-warning{% else %}btn-outline-warning{% endif %}">⏳ En cours</a>
    <a href="?statut=mise_en_demeure" class="btn {% if statut == 'mise_en_demeure' %}btn-danger{% else %}btn-outline-danger{% endif %}">⚠️ Mise en demeure</a>
    <a href="?statut=regularise" class="btn {% if statut == 'regularise' %}btn-success{% else %}btn-outline-success{% endif %}">✅ Regularisees</a>
    <a href="?statut=annulee" class="btn {% if statut == 'annulee' %}btn-secondary{% else %}btn-outline-secondary{% endif %}">🚫 Annulees</a>
  </div>

  <div class="card">
    <div class="card-body">
      {% if penalites %}
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead style="background:#f8f9fa;">
            <tr>
              <th>Reference</th>
              <th>Membre</th>
              <th>Tontine</th>
              <th>Mois</th>
              <th>Cotisation due</th>
              <th>Penalite 1.5%</th>
              <th>Total</th>
              <th>Mois impayes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {% for p in penalites %}
            <tr {% if p.mois_impaye >= 3 %}style="background:#fff5f5;"{% endif %}>
              <td><code>{{ p.reference }}</code></td>
              <td>
                <strong>{{ p.utilisateur.profil.nom_complet if p.utilisateur.profil else p.utilisateur.email }}</strong><br>
                <small class="text-muted">{{ p.utilisateur.email }}</small>
              </td>
              <td><span class="badge" style="background:#1a1a2e;color:#f0a500;">{{ p.tontine.code }}</span></td>
              <td><strong>{{ p.mois_reference }}</strong></td>
              <td>{{ "{:,.0f}".format(p.montant_du) }} FCFA</td>
              <td style="color:#e74c3c;font-weight:600;">{{ "{:,.0f}".format(p.montant_penalite) }} FCFA</td>
              <td style="font-weight:700;">{{ "{:,.0f}".format(p.montant_du + p.montant_penalite) }} FCFA</td>
              <td>
                {% if p.mois_impaye >= 3 %}
                <span class="badge bg-danger">{{ p.mois_impaye }} mois ⚠️ POURSUITE</span>
                {% elif p.mois_impaye == 2 %}
                <span class="badge bg-warning text-dark">{{ p.mois_impaye }} mois</span>
                {% else %}
                <span class="badge bg-secondary">{{ p.mois_impaye }} mois</span>
                {% endif %}
              </td>
              <td>
                {% if statut in ['en_cours', 'mise_en_demeure'] %}
                <form method="POST" action="{{ url_for('admin.regulariser_penalite', pen_id=p.id) }}" style="display:inline;">
                  <button type="submit" class="btn btn-sm btn-success" onclick="return confirm('Regulariser cette penalite ? Le montant sera debite du solde.')">✅ Regulariser</button>
                </form>
                <button class="btn btn-sm btn-outline-danger ms-1" data-bs-toggle="modal" data-bs-target="#annulModal{{ p.id }}">🚫 Annuler</button>
                <div class="modal fade" id="annulModal{{ p.id }}" tabindex="-1">
                  <div class="modal-dialog"><div class="modal-content">
                    <div class="modal-header"><h5 class="modal-title">Annuler la penalite</h5></div>
                    <form method="POST" action="{{ url_for('admin.annuler_penalite', pen_id=p.id) }}">
                      <div class="modal-body">
                        <p>Penalite <strong>{{ p.reference }}</strong> — {{ p.mois_reference }}</p>
                        <label class="form-label">Motif de l annulation</label>
                        <textarea name="note" class="form-control" rows="2" placeholder="Ex: Accord amiable..." required></textarea>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                        <button type="submit" class="btn btn-danger">Confirmer</button>
                      </div>
                    </form>
                  </div></div>
                </div>
                {% elif statut == 'regularise' %}
                <span style="color:#27ae60;font-size:0.85rem;">✅ {{ p.regularise_le.strftime('%d/%m/%Y') if p.regularise_le else '-' }}</span>
                {% else %}
                <span style="color:#999;font-size:0.85rem;">🚫 {{ p.note_admin or '-' }}</span>
                {% endif %}
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {% else %}
      <div class="text-center py-5">
        <div style="font-size:3rem;">✅</div>
        <p class="text-muted mt-2">Aucune penalite {{ statut.replace("_", " ") }}.</p>
      </div>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}"""

open("app/templates/admin/penalites.html", "w", encoding="utf-8").write(penalites_html)
print("OK penalites.html!")

# Template tableau_de_bord.html
tableau_html = """{% extends "base.html" %}
{% block title %}Tableau de bord Admin - TontineSecure{% endblock %}
{% block content %}
<div class="fade-in">
  <h1 class="page-title">Tableau de bord Administrateur</h1>
  <p class="page-subtitle">Vue complete de la plateforme en temps reel</p>

  <!-- KPIs principaux -->
  <div class="row g-3 mb-4">
    <div class="col-md-3">
      <div class="card text-center p-3" style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:16px;">
        <div style="color:#f0a500;font-size:0.8rem;font-weight:600;">TOTAL EN CAISSE</div>
        <div style="font-size:1.6rem;font-weight:700;margin:6px 0;">{{ "{:,.0f}".format(total_soldes) }}</div>
        <div style="color:#aaa;font-size:0.8rem;">FCFA</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card text-center p-3" style="border-left:4px solid #27ae60;">
        <div style="font-size:0.8rem;color:#666;font-weight:600;">COTISATIONS COLLECTEES</div>
        <div style="font-size:1.5rem;font-weight:700;color:#27ae60;">{{ "{:,.0f}".format(total_cotisations) }}</div>
        <div style="font-size:0.8rem;color:#999;">FCFA total</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card text-center p-3" style="border-left:4px solid #e74c3c;">
        <div style="font-size:0.8rem;color:#666;font-weight:600;">PENALITES DUES</div>
        <div style="font-size:1.5rem;font-weight:700;color:#e74c3c;">{{ "{:,.0f}".format(total_penalites_dues) }}</div>
        <div style="font-size:0.8rem;color:#999;">FCFA a recouvrer</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card text-center p-3" style="border-left:4px solid #f0a500;">
        <div style="font-size:0.8rem;color:#666;font-weight:600;">TONTINES ACTIVES</div>
        <div style="font-size:1.5rem;font-weight:700;color:#f0a500;">{{ tontines_actives }}</div>
        <div style="font-size:0.8rem;color:#999;">en cours</div>
      </div>
    </div>
  </div>

  <!-- Alertes urgentes -->
  <div class="row g-3 mb-4">
    {% if recharges_attente > 0 %}
    <div class="col-md-4">
      <a href="{{ url_for('admin.gerer_recharges') }}" style="text-decoration:none;">
        <div class="card p-3" style="border-left:4px solid #f0a500;background:#fffbf0;cursor:pointer;">
          <div class="d-flex align-items-center gap-3">
            <div style="font-size:2rem;">💳</div>
            <div>
              <div style="font-size:1.4rem;font-weight:700;color:#f0a500;">{{ recharges_attente }}</div>
              <div style="font-size:0.85rem;color:#666;">Recharges en attente</div>
            </div>
          </div>
        </div>
      </a>
    </div>
    {% endif %}
    {% if kyc_attente > 0 %}
    <div class="col-md-4">
      <a href="{{ url_for('admin.utilisateurs') }}" style="text-decoration:none;">
        <div class="card p-3" style="border-left:4px solid #3498db;background:#f0f8ff;cursor:pointer;">
          <div class="d-flex align-items-center gap-3">
            <div style="font-size:2rem;">🪪</div>
            <div>
              <div style="font-size:1.4rem;font-weight:700;color:#3498db;">{{ kyc_attente }}</div>
              <div style="font-size:0.85rem;color:#666;">KYC a verifier</div>
            </div>
          </div>
        </div>
      </a>
    </div>
    {% endif %}
    {% if mises_en_demeure > 0 %}
    <div class="col-md-4">
      <a href="{{ url_for('admin.gerer_penalites') }}?statut=mise_en_demeure" style="text-decoration:none;">
        <div class="card p-3" style="border-left:4px solid #e74c3c;background:#fff5f5;cursor:pointer;">
          <div class="d-flex align-items-center gap-3">
            <div style="font-size:2rem;">⚖️</div>
            <div>
              <div style="font-size:1.4rem;font-weight:700;color:#e74c3c;">{{ mises_en_demeure }}</div>
              <div style="font-size:0.85rem;color:#666;">Mises en demeure</div>
            </div>
          </div>
        </div>
      </a>
    </div>
    {% endif %}
  </div>

  <!-- Membres -->
  <div class="row g-3 mb-4">
    <div class="col-md-4">
      <div class="card p-3 text-center">
        <div style="font-size:2rem;">👥</div>
        <div style="font-size:1.5rem;font-weight:700;color:#1a1a2e;">{{ total_membres }}</div>
        <small class="text-muted">Total membres inscrits</small>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card p-3 text-center">
        <div style="font-size:2rem;">✅</div>
        <div style="font-size:1.5rem;font-weight:700;color:#27ae60;">{{ membres_actifs }}</div>
        <small class="text-muted">Membres actifs en tontine</small>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card p-3 text-center">
        <div style="font-size:2rem;">🚫</div>
        <div style="font-size:1.5rem;font-weight:700;color:#e74c3c;">{{ membres_suspendus }}</div>
        <small class="text-muted">Membres suspendus</small>
      </div>
    </div>
  </div>

  <!-- Tableau retardataires -->
  {% if retardataires %}
  <div class="card">
    <div class="card-body">
      <h5 style="font-family:Playfair Display,serif;color:#1a1a2e;margin-bottom:1rem;">⚠️ Retardataires - Action requise</h5>
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead style="background:#fff5f5;">
            <tr>
              <th>Membre</th>
              <th>Email</th>
              <th>Mois impayes</th>
              <th>Total du</th>
              <th>Statut</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {% for r in retardataires %}
            <tr {% if r.en_poursuite %}style="background:#fff5f5;"{% endif %}>
              <td><strong>{{ r.nom }}</strong></td>
              <td><small>{{ r.email }}</small></td>
              <td>
                {% if r.nb_impayes >= 3 %}
                <span class="badge bg-danger">{{ r.nb_impayes }} mois</span>
                {% else %}
                <span class="badge bg-warning text-dark">{{ r.nb_impayes }} mois</span>
                {% endif %}
              </td>
              <td><strong style="color:#e74c3c;">{{ "{:,.0f}".format(r.total_du) }} FCFA</strong></td>
              <td>
                {% if r.en_poursuite %}
                <span style="color:#e74c3c;font-weight:600;font-size:0.85rem;">⚖️ Poursuites possibles</span>
                {% else %}
                <span style="color:#f0a500;font-size:0.85rem;">⏳ En retard</span>
                {% endif %}
              </td>
              <td>
                <a href="{{ url_for('admin.gerer_penalites') }}?statut=en_cours" class="btn btn-sm btn-outline-danger">Voir penalites</a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  {% endif %}
</div>
{% endblock %}"""

open("app/templates/admin/tableau_de_bord.html", "w", encoding="utf-8").write(tableau_html)
print("OK tableau_de_bord.html!")
