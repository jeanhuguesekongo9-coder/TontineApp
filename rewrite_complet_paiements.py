import os

# Réécriture complète du module paiements
texte = """# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
import os
from ..models import db, Solde, Recharge, Transaction, Notification

paiements = Blueprint("paiements", __name__)

TAUX_FRAIS = 0.015  # 1.5% de frais sur chaque recharge

RESEAUX = {
    "wave_sn": {
        "nom": "Wave Sénégal",
        "type": "link",
        "base_url": "https://pay.wave.com/m/M_sn_XhdrMMWqgQ6I/c/sn/?amount=",
        "numero": "+221 78 538 53 10",
        "couleur": "#1DC8EE",
    },
    "wave_ci": {
        "nom": "Wave Côte d'Ivoire",
        "type": "link",
        "base_url": "https://pay.wave.com/m/M_sn_XhdrMMWqgQ6I/c/sn/?amount=",
        "numero": "+225 05 84 02 23 23",
        "couleur": "#1DC8EE",
    },
    "orange_sn": {
        "nom": "Orange Money Sénégal",
        "type": "ussd",
        "ussd_pattern": "*144*1*221785385310*{montant}#",
        "numero": "+221 78 538 53 10",
        "couleur": "#FF6600",
    },
    "orange_ci": {
        "nom": "Orange Money CI",
        "type": "ussd",
        "ussd_pattern": "*144*1*2250708224241*{montant}#",
        "numero": "+225 07 08 22 42 41",
        "couleur": "#FF6600",
    },
    "mtn_ci": {
        "nom": "MTN MoMo CI",
        "type": "ussd",
        "ussd_pattern": "*133*1*2250584022323*{montant}#",
        "numero": "+225 05 84 02 23 23",
        "couleur": "#FFCC00",
    },
}

def get_ou_creer_solde(user_id):
    solde = Solde.query.filter_by(user_id=user_id).first()
    if not solde:
        solde = Solde(user_id=user_id, montant=0.0)
        db.session.add(solde)
        db.session.commit()
    return solde

def calculer_frais(montant):
    frais = round(montant * TAUX_FRAIS)
    return {"net": montant, "frais": frais, "total": montant + frais}

@paiements.route("/")
@login_required
def dashboard():
    solde = get_ou_creer_solde(current_user.id)
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(20).all()
    recharges = Recharge.query.filter_by(user_id=current_user.id).order_by(Recharge.created_at.desc()).limit(10).all()
    return render_template("paiements/dashboard.html", solde=solde, transactions=transactions, recharges=recharges, reseaux=RESEAUX)

@paiements.route("/recharger", methods=["GET", "POST"])
@login_required
def recharger():
    if request.method == "POST":
        montant_net = float(request.form.get("montant", 0))
        reseau = request.form.get("reseau", "")
        numero = request.form.get("numero_telephone", "").strip()
        reference_transaction = request.form.get("reference_transaction", "").strip()
        capture = request.files.get("capture")
        if montant_net < 1000:
            flash("Montant minimum 1 000 FCFA.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not reseau or reseau not in RESEAUX:
            flash("Réseau invalide.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not numero:
            flash("Numéro de téléphone obligatoire.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        if not capture or not capture.filename:
            flash("La capture du transfert est obligatoire.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        ext = capture.filename.rsplit('.', 1)[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'pdf']:
            flash("Format capture invalide. JPG, PNG ou PDF uniquement.", "danger")
            return render_template("paiements/recharger.html", reseaux=RESEAUX)
        import secrets
        capture_filename = f"capture_{secrets.token_hex(8)}.{ext}"
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'captures')
        os.makedirs(upload_dir, exist_ok=True)
        capture.save(os.path.join(upload_dir, capture_filename))
        calc = calculer_frais(montant_net)
        recharge = Recharge(
            reference=Recharge.generer_reference(),
            user_id=current_user.id,
            montant=montant_net,
            reseau=reseau,
            numero_telephone=numero,
            reference_transaction=reference_transaction or "A_VERIFIER",
            statut="en_attente",
            note_admin=capture_filename
        )
        db.session.add(recharge)
        db.session.commit()
        notif = Notification(
            user_id=current_user.id,
            titre="Recharge en attente de validation",
            message=f"Votre recharge de {montant_net:,.0f} FCFA nets (+ {calc['frais']:,.0f} FCFA de frais) via {RESEAUX[reseau]['nom']} est en cours de vérification. Validation sous 24h maximum.",
            type_notif="info",
            lien=url_for("paiements.dashboard")
        )
        db.session.add(notif)
        db.session.commit()
        flash(f"Recharge de {montant_net:,.0f} FCFA soumise avec succès ! Vérification par notre équipe sous 24h.", "success")
        return redirect(url_for("paiements.dashboard"))
    return render_template("paiements/recharger.html", reseaux=RESEAUX)

@paiements.route("/facture/<string:reference>")
@login_required
def facture(reference):
    transaction = Transaction.query.filter_by(reference=reference, user_id=current_user.id).first_or_404()
    return render_template("paiements/facture.html", transaction=transaction)

@paiements.route("/ma-tontine")
@login_required
def ma_tontine():
    from ..models import MembreTontine, Penalite
    memberships = MembreTontine.query.filter_by(user_id=current_user.id).all()
    penalites_actives = Penalite.query.filter(
        Penalite.user_id == current_user.id,
        Penalite.statut.in_(["en_cours", "mise_en_demeure"])
    ).all()
    return render_template("paiements/ma_tontine.html",
        memberships=memberships,
        penalites_actives=penalites_actives)
"""
open("app/paiements/__init__.py", "w", encoding="utf-8").write(texte)
print("OK paiements/__init__.py!")

# Réécriture complète du template recharger.html
template = """{% extends "base.html" %}
{% block title %}Recharger mon compte - TontineSecure{% endblock %}
{% block content %}
<div style="max-width:620px;margin:0 auto;" class="fade-in">
  <h1 class="page-title">Recharger mon compte</h1>
  <p class="page-subtitle">Choisissez votre moyen de paiement</p>

  <div class="card">
    <div class="card-body p-4">
      <form method="POST" enctype="multipart/form-data">

        <!-- Choix réseau -->
        <div class="mb-4">
          <label class="form-label fw-semibold">Réseau de paiement <span style="color:#e74c3c;">*</span></label>
          <div class="row g-2">

            <div class="col-6">
              <input type="radio" name="reseau" id="wave_sn" value="wave_sn" class="d-none reseau-radio" required>
              <label for="wave_sn" class="reseau-card w-100 text-center p-3" style="border:2px solid #eee;border-radius:12px;cursor:pointer;transition:all 0.2s;">
                <div style="width:52px;height:52px;margin:0 auto 6px;border-radius:12px;background:#1DC8EE;display:flex;align-items:center;justify-content:center;">
                  <svg width="32" height="20" viewBox="0 0 120 60" fill="none"><path d="M10 50 Q30 10 50 30 Q70 50 90 10 Q100 5 110 20" stroke="white" stroke-width="10" fill="none" stroke-linecap="round"/></svg>
                </div>
                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Sénégal</div>
                <div style="font-size:0.72rem;color:#1DC8EE;font-weight:600;">🇸🇳 Lien direct</div>
              </label>
            </div>

            <div class="col-6">
              <input type="radio" name="reseau" id="wave_ci" value="wave_ci" class="d-none reseau-radio">
              <label for="wave_ci" class="reseau-card w-100 text-center p-3" style="border:2px solid #eee;border-radius:12px;cursor:pointer;transition:all 0.2s;">
                <div style="width:52px;height:52px;margin:0 auto 6px;border-radius:12px;background:#1DC8EE;display:flex;align-items:center;justify-content:center;">
                  <svg width="32" height="20" viewBox="0 0 120 60" fill="none"><path d="M10 50 Q30 10 50 30 Q70 50 90 10 Q100 5 110 20" stroke="white" stroke-width="10" fill="none" stroke-linecap="round"/></svg>
                </div>
                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Côte d'Ivoire</div>
                <div style="font-size:0.72rem;color:#1DC8EE;font-weight:600;">🇨🇮 Lien direct</div>
              </label>
            </div>

            <div class="col-6">
              <input type="radio" name="reseau" id="orange_sn" value="orange_sn" class="d-none reseau-radio">
              <label for="orange_sn" class="reseau-card w-100 text-center p-3" style="border:2px solid #eee;border-radius:12px;cursor:pointer;transition:all 0.2s;">
                <div style="width:52px;height:52px;margin:0 auto 6px;border-radius:50%;background:#FF6600;display:flex;align-items:center;justify-content:center;">
                  <span style="color:#fff;font-weight:900;font-size:1.3rem;">O</span>
                </div>
                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money SN</div>
                <div style="font-size:0.72rem;color:#FF6600;font-weight:600;">🇸🇳 +221 78 538 53 10</div>
              </label>
            </div>

            <div class="col-6">
              <input type="radio" name="reseau" id="orange_ci" value="orange_ci" class="d-none reseau-radio">
              <label for="orange_ci" class="reseau-card w-100 text-center p-3" style="border:2px solid #eee;border-radius:12px;cursor:pointer;transition:all 0.2s;">
                <div style="width:52px;height:52px;margin:0 auto 6px;border-radius:50%;background:#FF6600;display:flex;align-items:center;justify-content:center;">
                  <span style="color:#fff;font-weight:900;font-size:1.3rem;">O</span>
                </div>
                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money CI</div>
                <div style="font-size:0.72rem;color:#FF6600;font-weight:600;">🇨🇮 +225 07 08 22 42 41</div>
              </label>
            </div>

            <div class="col-6">
              <input type="radio" name="reseau" id="mtn_ci" value="mtn_ci" class="d-none reseau-radio">
              <label for="mtn_ci" class="reseau-card w-100 text-center p-3" style="border:2px solid #eee;border-radius:12px;cursor:pointer;transition:all 0.2s;">
                <div style="width:52px;height:52px;margin:0 auto 6px;border-radius:12px;background:#FFCC00;display:flex;align-items:center;justify-content:center;">
                  <span style="color:#1a1a2e;font-weight:900;font-size:0.8rem;">MTN</span>
                </div>
                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">MTN MoMo CI</div>
                <div style="font-size:0.72rem;color:#e6a800;font-weight:600;">🇨🇮 +225 05 84 02 23 23</div>
              </label>
            </div>

          </div>
        </div>

        <!-- Montant souhaité -->
        <div class="mb-4">
          <label class="form-label fw-semibold">Montant à créditer sur votre solde (FCFA) <span style="color:#e74c3c;">*</span></label>
          <input type="number" name="montant" id="montant_input" class="form-control" placeholder="Ex: 50 000" min="1000" step="500" required>
          <div class="form-text">Montant minimum : 1 000 FCFA</div>
          <div class="row g-2 mt-2">
            {% for m in [5000, 10000, 25000, 50000, 100000, 200000] %}
            <div class="col-4">
              <button type="button" class="btn btn-outline-secondary w-100 btn-montant" style="font-size:0.8rem;" data-montant="{{ m }}">{{ "{:,.0f}".format(m) }}</button>
            </div>
            {% endfor %}
          </div>
        </div>

        <!-- Zone récapitulatif frais + bouton payer -->
        <div id="zone_payer" style="display:none;margin-bottom:1.5rem;">

          <!-- Récapitulatif frais -->
          <div id="recap_frais" style="background:linear-gradient(135deg,#f8f9fa,#e9ecef);border-radius:12px;padding:16px;margin-bottom:12px;">
            <div style="font-size:0.82rem;color:#666;font-weight:600;margin-bottom:8px;">RÉCAPITULATIF DE VOTRE RECHARGE</div>
            <div class="d-flex justify-content-between mb-1">
              <span style="color:#555;">Montant crédité sur votre solde</span>
              <span id="recap_net" style="font-weight:700;color:#1a1a2e;"></span>
            </div>
            <div class="d-flex justify-content-between mb-1">
              <span style="color:#555;">Frais de service TontineSecure (1,5 %)</span>
              <span id="recap_frais_val" style="font-weight:600;color:#e74c3c;"></span>
            </div>
            <div style="border-top:1px solid #dee2e6;margin:8px 0;"></div>
            <div class="d-flex justify-content-between">
              <span style="font-weight:700;color:#1a1a2e;">Total à envoyer</span>
              <span id="recap_total" style="font-weight:700;color:#27ae60;font-size:1.1rem;"></span>
            </div>
          </div>

          <!-- Bouton Wave -->
          <a id="btn_wave" href="#" target="_blank"
            style="display:none;background:#1DC8EE;color:#fff;border-radius:12px;padding:14px 20px;
                   font-weight:700;font-size:1rem;text-align:center;text-decoration:none;
                   width:100%;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;">
            🌊 Payer avec Wave →
          </a>
          <div id="msg_wave" style="display:none;background:#e8f8ff;border:1px solid #1DC8EE;border-radius:10px;padding:12px;font-size:0.88rem;color:#1a1a2e;line-height:1.6;margin-bottom:10px;">
          </div>

          <!-- Bouton USSD -->
          <a id="btn_ussd" href="#"
            style="display:none;border-radius:12px;padding:14px 20px;font-weight:700;font-size:1rem;
                   text-align:center;text-decoration:none;color:#fff;width:100%;
                   align-items:center;justify-content:center;gap:8px;margin-bottom:10px;">
            📞 Composer le code de paiement →
          </a>
          <div id="msg_ussd" style="display:none;background:#fff8f0;border:1px solid #f0a500;border-radius:10px;padding:15px;font-size:0.9rem;color:#1a1a2e;line-height:1.8;margin-bottom:10px;">
          </div>

        </div>

        <!-- Numéro de téléphone -->
        <div class="mb-4">
          <label class="form-label fw-semibold">Votre numéro de téléphone <span style="color:#e74c3c;">*</span></label>
          <input type="text" name="numero_telephone" class="form-control" placeholder="+221 77 XXX XX XX" required>
          <div class="form-text">Le numéro depuis lequel vous effectuez le transfert</div>
        </div>

        <!-- Référence transaction -->
        <div class="mb-4">
          <label class="form-label fw-semibold">Référence de transaction <span style="color:#999;font-size:0.82rem;">(optionnel)</span></label>
          <input type="text" name="reference_transaction" class="form-control" placeholder="Ex : TXN123456789">
          <div class="form-text">Visible dans le SMS de confirmation de votre opération</div>
        </div>

        <!-- Upload capture obligatoire -->
        <div class="mb-4">
          <label class="form-label fw-semibold">Capture de confirmation du transfert <span style="color:#e74c3c;">*</span></label>
          <div onclick="document.getElementById('capture_file').click()"
               style="border:2px dashed #dee2e6;border-radius:12px;padding:25px;text-align:center;
                      cursor:pointer;transition:all 0.2s;"
               onmouseover="this.style.borderColor='#f0a500';this.style.background='#fffbf0';"
               onmouseout="this.style.borderColor='#dee2e6';this.style.background='#fff';">
            <div style="font-size:2.5rem;">📸</div>
            <div style="color:#555;font-weight:600;margin-top:8px;">Cliquez pour uploader la capture</div>
            <div style="color:#999;font-size:0.82rem;margin-top:4px;">JPG, PNG ou PDF — Max 5 MB</div>
            <div id="nom_capture" style="color:#27ae60;font-size:0.88rem;margin-top:8px;font-weight:600;"></div>
          </div>
          <input type="file" id="capture_file" name="capture" accept=".jpg,.jpeg,.png,.pdf"
                 style="display:none;"
                 onchange="document.getElementById('nom_capture').textContent = this.files[0] ? '✅ ' + this.files[0].name : ''">
          <div class="form-text">📌 La capture est obligatoire pour valider votre recharge.</div>
        </div>

        <button type="submit" class="btn-or w-100" style="padding:0.9rem;font-size:1rem;border-radius:12px;">
          ✅ Soumettre ma recharge
        </button>

      </form>
    </div>
  </div>
</div>

<script>
var DATA = {
  wave_sn:   {type:"link", url:"https://pay.wave.com/m/M_sn_XhdrMMWqgQ6I/c/sn/?amount=", couleur:"#1DC8EE", numero:"+221 78 538 53 10",  ussd:""},
  wave_ci:   {type:"link", url:"https://pay.wave.com/m/M_sn_XhdrMMWqgQ6I/c/sn/?amount=", couleur:"#1DC8EE", numero:"+225 05 84 02 23 23", ussd:""},
  orange_sn: {type:"ussd", url:"", couleur:"#FF6600", numero:"+221 78 538 53 10",  ussd:"*144*1*221785385310*"},
  orange_ci: {type:"ussd", url:"", couleur:"#FF6600", numero:"+225 07 08 22 42 41", ussd:"*144*1*2250708224241*"},
  mtn_ci:    {type:"ussd", url:"", couleur:"#FFCC00", numero:"+225 05 84 02 23 23", ussd:"*133*1*2250584022323*"}
};

var reseau_actif = null;

document.querySelectorAll('.reseau-radio').forEach(function(r) {
  r.addEventListener('change', function() {
    reseau_actif = this.value;
    document.querySelectorAll('.reseau-card').forEach(function(c) {
      c.style.borderColor = '#eee';
      c.style.background = '#fff';
    });
    var lbl = document.querySelector('label[for="' + reseau_actif + '"]');
    lbl.style.borderColor = DATA[reseau_actif].couleur;
    lbl.style.background = DATA[reseau_actif].couleur + '18';
    majBouton();
  });
});

document.getElementById('montant_input').addEventListener('input', majBouton);
document.querySelectorAll('.btn-montant').forEach(function(b) {
  b.addEventListener('click', function() {
    document.getElementById('montant_input').value = this.dataset.montant;
    majBouton();
  });
});

function formater(n) {
  return parseInt(n).toLocaleString('fr-FR') + ' FCFA';
}

function majBouton() {
  var montant = parseInt(document.getElementById('montant_input').value);
  var zone = document.getElementById('zone_payer');
  if (!reseau_actif || !montant || montant < 1000) {
    zone.style.display = 'none';
    return;
  }
  var frais = Math.ceil(montant * 0.015);
  var total = montant + frais;
  var d = DATA[reseau_actif];

  // Récapitulatif
  zone.style.display = 'block';
  document.getElementById('recap_net').textContent = formater(montant);
  document.getElementById('recap_frais_val').textContent = '+ ' + formater(frais);
  document.getElementById('recap_total').textContent = formater(total);

  var btnW = document.getElementById('btn_wave');
  var btnU = document.getElementById('btn_ussd');
  var msgW = document.getElementById('msg_wave');
  var msgU = document.getElementById('msg_ussd');

  if (d.type === 'link') {
    btnW.style.display = 'flex';
    btnU.style.display = 'none';
    msgW.style.display = 'block';
    msgU.style.display = 'none';
    btnW.href = d.url + total;
    btnW.style.background = d.couleur;
    btnW.innerHTML = '🌊 Payer ' + formater(total) + ' avec Wave →';
    msgW.innerHTML = '💡 En cliquant sur ce bouton, vous serez redirigé vers <strong>Wave</strong> pour confirmer un paiement de <strong>' + formater(total) + '</strong>. Ce montant comprend <strong>' + formater(montant) + '</strong> crédités sur votre solde TontineSecure + <strong>' + formater(frais) + '</strong> de frais de service (1,5 %). Une fois le paiement confirmé sur Wave, notre équipe validera votre recharge sous 24h.';
  } else {
    btnW.style.display = 'none';
    btnU.style.display = 'flex';
    msgW.style.display = 'none';
    msgU.style.display = 'block';
    var code = encodeURIComponent(d.ussd + total + '#');
    btnU.href = 'tel:' + code;
    btnU.style.background = d.couleur;
    btnU.style.color = d.couleur === '#FFCC00' ? '#1a1a2e' : '#fff';
    btnU.innerHTML = '📞 Composer le code pour ' + formater(total) + ' →';
    msgU.innerHTML = '💡 Veuillez transférer <strong>' + formater(total) + '</strong> au numéro <strong>' + d.numero + '</strong>.<br>Ce montant comprend :<ul style="margin:8px 0 0;padding-left:20px;"><li><strong>' + formater(montant) + '</strong> → crédités sur votre solde TontineSecure</li><li><strong>' + formater(frais) + '</strong> → frais de service TontineSecure (1,5 %)</li></ul>Après le transfert, uploadez la capture de confirmation ci-dessous. Notre équipe validera votre recharge sous <strong>24h maximum</strong>.';
  }
}
</script>
{% endblock %}"""

open("app/templates/paiements/recharger.html", "w", encoding="utf-8").write(template)
print("OK template recharger.html!")
