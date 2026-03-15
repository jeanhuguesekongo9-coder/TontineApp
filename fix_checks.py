content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

ancien_checks = """          <div class="form-check mb-2">
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
          </div>"""

nouveau_checks = """          <div class="form-check mb-2">
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
          </div>"""

content = content.replace(ancien_checks, nouveau_checks)

# Verifier le check3 et check4 et ajouter check5
idx3 = content.find("check3")
if idx3 >= 0:
    print("check3 trouve:")
    print(content[idx3-50:idx3+300])
