content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# 1. Mettre a jour les cases a cocher
ancien_cases = """          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check1">
            <label class="form-check-label" for="check1" style="font-size:0.9rem;color:#444;">
              J'ai lu et compris l'intégralité du contrat, notamment les articles sur les pénalités et les poursuites judiciaires.
            </label>
          </div>
          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check2">
            <label class="form-check-label" for="check2" style="font-size:0.9rem;color:#444;">
              J'accepte la garantie de paiement TontineSecure et les conditions d'anonymat entre membres.
            </label>
          </div>
          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check3">
            <label class="form-check-label" for="check3" style="font-size:0.9rem;color:#444;">
              Je m'engage à maintenir mon solde suffisant avant le 5 de chaque mois pour toute la durée de la tontine.
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="check4">
            <label class="form-check-label" for="check4" style="font-size:0.9rem;color:#444;">
              J'autorise TontineSecure à utiliser mes informations KYC dans le cadre d'éventuelles procédures de recouvrement.
            </label>
          </div>"""

nouveau_cases = """          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check1">
            <label class="form-check-label" for="check1" style="font-size:0.9rem;color:#444;">
              J'ai lu et compris l'intégralité du contrat, notamment les articles sur les pénalités, les frais de service et les poursuites judiciaires.
            </label>
          </div>
          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check2">
            <label class="form-check-label" for="check2" style="font-size:0.9rem;color:#444;">
              J'accepte les frais de service : 1,5 % sur chaque recharge (0,5 % fonds de garantie + 1 % TontineSecure) et les frais annuels de tenue de compte de 1 % du panier mensuel.
            </label>
          </div>
          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check3">
            <label class="form-check-label" for="check3" style="font-size:0.9rem;color:#444;">
              Je comprends que la garantie de paiement est activée uniquement lorsque le fonds de garantie de ma tontine atteint 20 % du panier mensuel.
            </label>
          </div>
          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check4">
            <label class="form-check-label" for="check4" style="font-size:0.9rem;color:#444;">
              Je m'engage à maintenir un solde suffisant avant le 5 de chaque mois pour toute la durée de la tontine, sous peine de pénalités de 1,5 % par mois de retard.
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="check5">
            <label class="form-check-label" for="check5" style="font-size:0.9rem;color:#444;">
              J'autorise TontineSecure à utiliser mes informations KYC dans le cadre d'éventuelles procédures de recouvrement judiciaire ou amiable.
            </label>
          </div>"""

content = content.replace(ancien_cases, nouveau_cases)

# 2. Ajouter la signature TontineSecure avant le bouton signer
ancien_btn = """        <form method="POST" action="{{ url_for('contrats.signer_contrat', tontine_id=tontine.id) }}">
          <button type="submit" id="btn_signer" onclick="return validerSignature()"
            style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border:none;
                   padding:15px 40px;border-radius:12px;font-size:1rem;font-weight:700;
                   cursor:pointer;width:100%;transition:all 0.3s;">
            ✍️ Je signe ce contrat et rejoins la tontine
          </button>
        </form>"""

nouveau_btn = """        <!-- Signatures -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;margin:30px 0;padding:20px;background:#f8f9fa;border-radius:12px;">
          <div style="text-align:center;border-right:1px solid #dee2e6;padding-right:20px;">
            <p style="font-size:0.8rem;color:#999;margin-bottom:10px;">SIGNATURE DU PARTICIPANT</p>
            <div style="border-bottom:2px solid #1a1a2e;height:50px;margin-bottom:8px;display:flex;align-items:flex-end;justify-content:center;">
              <span style="font-size:0.75rem;color:#aaa;padding-bottom:4px;">Signature électronique au moment de la validation</span>
            </div>
            <p style="font-size:0.85rem;font-weight:600;color:#1a1a2e;">{{ membre_nom }}</p>
            <p style="font-size:0.75rem;color:#666;">{{ membre_email }}</p>
          </div>
          <div style="text-align:center;padding-left:20px;">
            <p style="font-size:0.8rem;color:#999;margin-bottom:10px;">SIGNATURE DE TONTINESECURE</p>
            <div style="border-bottom:2px solid #f0a500;height:50px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;">
              <span style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:800;color:#f0a500;font-style:italic;">TontineSecure</span>
            </div>
            <p style="font-size:0.85rem;font-weight:600;color:#1a1a2e;">La Direction Générale</p>
            <p style="font-size:0.75rem;color:#666;">Société de gestion de tontines sécurisées</p>
            <div style="margin-top:8px;padding:6px 12px;background:#1a1a2e;border-radius:20px;display:inline-block;">
              <span style="color:#f0a500;font-size:0.7rem;font-weight:700;">CACHET OFFICIEL</span>
            </div>
          </div>
        </div>

        <form method="POST" action="{{ url_for('contrats.signer_contrat', tontine_id=tontine.id) }}">
          <button type="submit" id="btn_signer" onclick="return validerSignature()"
            style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border:none;
                   padding:15px 40px;border-radius:12px;font-size:1rem;font-weight:700;
                   cursor:pointer;width:100%;transition:all 0.3s;">
            ✍️ Je signe ce contrat et rejoins la tontine
          </button>
        </form>"""

content = content.replace(ancien_btn, nouveau_btn)

# 3. Mettre a jour le JS pour 5 cases
content = content.replace(
    "var cases = ['check1','check2','check3','check4'];",
    "var cases = ['check1','check2','check3','check4','check5'];"
)

open("app/templates/contrats/contrat.html", "w", encoding="utf-8").write(content)

# Verification
print("check5 present :", "check5" in content)
print("Signature TontineSecure present :", "CACHET OFFICIEL" in content)
print("JS 5 cases :", "check5" in content)
print("OK! Contrat mis a jour complet!")
