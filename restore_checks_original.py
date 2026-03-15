content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Remplacer les nouvelles cases par les originales + 1 case frais ajoutee
ancien = """          <div class="form-check mb-2">
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

nouveau = """          <div class="form-check mb-2">
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
          <div class="form-check mb-2">
            <input class="form-check-input" type="checkbox" id="check4">
            <label class="form-check-label" for="check4" style="font-size:0.9rem;color:#444;">
              J'autorise TontineSecure à utiliser mes informations KYC dans le cadre d'éventuelles procédures de recouvrement.
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="check5">
            <label class="form-check-label" for="check5" style="font-size:0.9rem;color:#444;">
              J'accepte les frais de service : 1,5 % sur chaque recharge (0,5 % fonds de garantie + 1 % TontineSecure) et les frais annuels de tenue de compte de 1 % du panier mensuel.
            </label>
          </div>"""

content = content.replace(ancien, nouveau)

# JS 5 cases
content = content.replace(
    "var cases = ['check1','check2','check3','check4','check5'];",
    "var cases = ['check1','check2','check3','check4','check5'];"
)

open("app/templates/contrats/contrat.html", "w", encoding="utf-8").write(content)
print("check5 present:", "check5" in content)
print("Forme originale restauree avec case frais ajoutee!")
