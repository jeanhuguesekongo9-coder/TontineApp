content = """{% extends "base.html" %}
{% block title %}Facture {{ transaction.reference }} - TontineSecure{% endblock %}
{% block content %}
<div style="max-width:600px;margin:0 auto;" class="fade-in">
  <div class="card" style="border-radius:20px;overflow:hidden;">
    <!-- Header facture -->
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:30px;text-align:center;">
      <h1 style="color:#f0a500;font-family:Playfair Display,serif;margin:0;">TontineSecure</h1>
      <p style="color:#fff;margin:5px 0 0;">
        {% if transaction.sens == 'credit' %}FACTURE DE CREDIT{% else %}FACTURE DE DEBIT{% endif %}
      </p>
    </div>
    <div class="card-body p-4">
      <!-- Montant -->
      <div class="text-center mb-4">
        {% if transaction.sens == 'credit' %}
        <div style="font-size:3rem;font-weight:700;color:#27ae60;">+{{ "{:,.0f}".format(transaction.montant) }} FCFA</div>
        <span class="badge" style="background:#d4edda;color:#27ae60;padding:5px 15px;border-radius:20px;">CREDIT</span>
        {% else %}
        <div style="font-size:3rem;font-weight:700;color:#e74c3c;">-{{ "{:,.0f}".format(transaction.montant) }} FCFA</div>
        <span class="badge" style="background:#f8d7da;color:#e74c3c;padding:5px 15px;border-radius:20px;">DEBIT</span>
        {% endif %}
      </div>
      <hr>
      <!-- Details -->
      <table class="table table-borderless">
        <tr>
          <td style="color:#999;">Reference</td>
          <td style="font-weight:600;"><code>{{ transaction.reference }}</code></td>
        </tr>
        <tr>
          <td style="color:#999;">Date</td>
          <td>{{ transaction.created_at.strftime('%d/%m/%Y a %H:%M') }}</td>
        </tr>
        <tr>
          <td style="color:#999;">Type</td>
          <td>{{ transaction.type_transaction|capitalize }}</td>
        </tr>
        <tr>
          <td style="color:#999;">Description</td>
          <td>{{ transaction.description or '-' }}</td>
        </tr>
        <tr>
          <td style="color:#999;">Solde avant</td>
          <td>{{ "{:,.0f}".format(transaction.solde_avant or 0) }} FCFA</td>
        </tr>
        <tr>
          <td style="color:#999;">Solde apres</td>
          <td style="font-weight:700;">{{ "{:,.0f}".format(transaction.solde_apres or 0) }} FCFA</td>
        </tr>
      </table>
      <hr>
      <div class="text-center" style="color:#999;font-size:0.8rem;">
        TontineSecure — Epargne collaborative securisee<br>
        Cote d Ivoire & Senegal
      </div>
      <div class="text-center mt-3">
        <button onclick="window.print()" class="btn-or" style="padding:10px 30px;">🖨️ Imprimer</button>
        <a href="{{ url_for('paiements.dashboard') }}" class="btn btn-outline-secondary ms-2" style="padding:10px 20px;">Retour</a>
      </div>
    </div>
  </div>
</div>
{% endblock %}"""
open("app/templates/paiements/facture.html", "w", encoding="utf-8").write(content)
print("OK!")
