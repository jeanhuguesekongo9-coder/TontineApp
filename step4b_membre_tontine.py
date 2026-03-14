# Template tontine anonymisee pour le membre
contenu = """{% extends "base.html" %}
{% block title %}Ma Tontine - TontineSecure{% endblock %}
{% block content %}
<div class="fade-in" style="max-width:700px;margin:0 auto;">
  <h1 class="page-title">Ma Tontine</h1>
  <p class="page-subtitle">Votre espace personnel et confidentiel</p>

  {% for mt in memberships %}
  {% set t = mt.tontine %}
  <div class="card mb-4" style="border-radius:20px;overflow:hidden;">

    <!-- Header tontine -->
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:25px;color:#fff;">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <div style="color:#f0a500;font-size:0.8rem;font-weight:600;letter-spacing:2px;">TONTINE</div>
          <div style="font-size:1.5rem;font-weight:700;">{{ t.code }}</div>
        </div>
        <div style="text-align:right;">
          {% if t.statut == 'en_cours' %}
          <span class="badge" style="background:#27ae60;padding:8px 14px;border-radius:20px;">● En cours</span>
          {% elif t.statut == 'recrutement' %}
          <span class="badge" style="background:#f0a500;padding:8px 14px;border-radius:20px;">● Recrutement</span>
          {% else %}
          <span class="badge" style="background:#666;padding:8px 14px;border-radius:20px;">{{ t.statut }}</span>
          {% endif %}
        </div>
      </div>
      <div class="row mt-3 g-3">
        <div class="col-4 text-center">
          <div style="font-size:1.8rem;font-weight:700;color:#f0a500;">{{ "{:,.0f}".format(t.montant_panier) }}</div>
          <div style="font-size:0.75rem;color:#aaa;">FCFA / cotisation</div>
        </div>
        <div class="col-4 text-center">
          <div style="font-size:1.8rem;font-weight:700;">{{ t.nombre_membres }}</div>
          <div style="font-size:0.75rem;color:#aaa;">membres au total</div>
        </div>
        <div class="col-4 text-center">
          <div style="font-size:1.8rem;font-weight:700;color:#1DC8EE;">
            #{{ mt.ordre_collecte if mt.ordre_collecte else '?' }}
          </div>
          <div style="font-size:0.75rem;color:#aaa;">votre position</div>
        </div>
      </div>
    </div>

    <div class="card-body p-4">

      <!-- Votre statut -->
      <div class="mb-4" style="background:#f8f9fa;border-radius:12px;padding:15px;">
        <h6 style="color:#1a1a2e;font-weight:700;margin-bottom:12px;">Votre statut dans cette tontine</h6>
        <div class="row g-2">
          <div class="col-6">
            <div style="font-size:0.8rem;color:#666;">Votre position</div>
            <div style="font-size:1.1rem;font-weight:700;color:#1a1a2e;">
              Membre #{{ mt.ordre_collecte if mt.ordre_collecte else 'Non defini' }} sur {{ t.nombre_membres }}
            </div>
          </div>
          <div class="col-6">
            <div style="font-size:0.8rem;color:#666;">Statut</div>
            <div style="font-size:1rem;font-weight:600;">
              {% if mt.statut == 'actif' %}
              <span style="color:#27ae60;">✅ Actif</span>
              {% elif mt.statut == 'suspendu' %}
              <span style="color:#e74c3c;">🚫 Suspendu</span>
              {% else %}
              <span style="color:#666;">{{ mt.statut }}</span>
              {% endif %}
            </div>
          </div>
          <div class="col-6 mt-2">
            <div style="font-size:0.8rem;color:#666;">Panier recu</div>
            <div style="font-size:1rem;font-weight:600;">
              {% if mt.a_recu %}
              <span style="color:#27ae60;">✅ Oui</span>
              {% else %}
              <span style="color:#f0a500;">⏳ En attente</span>
              {% endif %}
            </div>
          </div>
          <div class="col-6 mt-2">
            <div style="font-size:0.8rem;color:#666;">Membre depuis</div>
            <div style="font-size:0.9rem;font-weight:600;color:#1a1a2e;">
              {{ mt.date_adhesion.strftime('%d/%m/%Y') }}
            </div>
          </div>
        </div>
      </div>

      <!-- Membres anonymes -->
      <div class="mb-4">
        <h6 style="color:#1a1a2e;font-weight:700;margin-bottom:12px;">
          👥 Composition du groupe
          <span style="font-size:0.75rem;color:#999;font-weight:400;margin-left:8px;">Les identites sont confidentielles</span>
        </h6>
        <div class="row g-2">
          {% for i in range(1, t.nombre_membres + 1) %}
          <div class="col-6 col-md-4">
            <div style="background:{% if mt.ordre_collecte == i %}linear-gradient(135deg,#1a1a2e,#16213e){% else %}#f8f9fa{% endif %};border-radius:10px;padding:10px;text-align:center;">
              <div style="font-size:1.2rem;">
                {% if mt.ordre_collecte == i %}👤{% else %}🔒{% endif %}
              </div>
              <div style="font-size:0.8rem;font-weight:700;color:{% if mt.ordre_collecte == i %}#f0a500{% else %}#666{% endif %};">
                Membre #{{ i }}
                {% if mt.ordre_collecte == i %}<br><span style="font-size:0.7rem;color:#1DC8EE;">(Vous)</span>{% endif %}
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
        <div style="background:#f0f8ff;border-radius:10px;padding:12px;margin-top:12px;">
          <small style="color:#666;">🔐 Pour garantir la confidentialite et la securite de tous les membres, les identites sont masquees. Seule votre position vous est visible.</small>
        </div>
      </div>

      <!-- Penalites du membre -->
      {% if penalites_actives %}
      <div style="background:#fff5f5;border:1px solid #ffcccc;border-radius:12px;padding:15px;margin-bottom:1rem;">
        <h6 style="color:#e74c3c;font-weight:700;">⚠️ Penalites en cours</h6>
        {% for pen in penalites_actives %}
        {% if pen.tontine_id == t.id %}
        <div style="font-size:0.9rem;color:#555;margin-bottom:6px;">
          Mois {{ pen.mois_reference }} — Cotisation: <strong>{{ "{:,.0f}".format(pen.montant_du) }} FCFA</strong>
          + Penalite 1.5%: <strong style="color:#e74c3c;">{{ "{:,.0f}".format(pen.montant_penalite) }} FCFA</strong>
          = <strong>{{ "{:,.0f}".format(pen.montant_du + pen.montant_penalite) }} FCFA</strong>
          {% if pen.mois_impaye >= 3 %}
          <span class="badge bg-danger ms-2">⚖️ Mise en demeure</span>
          {% endif %}
        </div>
        {% endif %}
        {% endfor %}
        <a href="{{ url_for('paiements.recharger') }}" class="btn btn-sm btn-danger mt-2">Recharger maintenant</a>
      </div>
      {% endif %}

    </div>
  </div>
  {% else %}
  <div class="card text-center p-5">
    <div style="font-size:3rem;">🔍</div>
    <p class="text-muted mt-2">Vous n etes membre d aucune tontine pour le moment.</p>
    <a href="{{ url_for('tontines.liste') }}" class="btn-or mt-3" style="display:inline-block;padding:10px 25px;">Rejoindre une tontine</a>
  </div>
  {% endfor %}
</div>
{% endblock %}"""

open("app/templates/paiements/ma_tontine.html", "w", encoding="utf-8").write(contenu)
print("OK ma_tontine.html!")
