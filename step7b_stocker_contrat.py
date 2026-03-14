# Mettre a jour la route signer_contrat pour stocker le HTML complet
content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()

nouvelle_logique = """
def generer_contenu_html(membre_nom, membre_email, tontine, reference_contrat, ip_signature, date_signature):
    from datetime import datetime
    return f\"\"\"<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Contrat TontineSecure — {reference_contrat}</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 900px; margin: 0 auto; padding: 40px; color: #222; }}
    h1 {{ text-align: center; color: #1a1a2e; font-size: 1.8rem; }}
    .header {{ background: #1a1a2e; color: white; padding: 30px; text-align: center; border-radius: 12px; margin-bottom: 30px; }}
    .header h1 {{ color: #f0a500; margin: 0; }}
    .header p {{ color: #aaa; margin: 5px 0 0; }}
    .badge-contrat {{ background: rgba(240,165,0,0.2); border: 1px solid #f0a500; padding: 8px 20px; border-radius: 6px; display: inline-block; margin-top: 12px; color: #f0a500; font-weight: 700; }}
    .meta {{ background: #f8f9fa; border-radius: 8px; padding: 15px 20px; margin-bottom: 25px; }}
    .meta table {{ width: 100%; border-collapse: collapse; }}
    .meta td {{ padding: 5px 10px; }}
    .meta td:first-child {{ font-weight: 700; color: #888; font-size: 0.85rem; width: 200px; }}
    h2 {{ color: #1a1a2e; font-size: 1.1rem; border-bottom: 2px solid #f0a500; padding-bottom: 6px; margin-top: 30px; }}
    p {{ line-height: 1.8; text-align: justify; }}
    ul, ol {{ line-height: 2; }}
    .garantie {{ background: #f0fff4; border: 2px solid #27ae60; border-radius: 8px; padding: 15px 20px; margin: 15px 0; }}
    .penalite {{ background: #fff5f5; border: 2px solid #e74c3c; border-radius: 8px; padding: 15px 20px; margin: 15px 0; }}
    .escalade {{ background: #fff5f5; border-left: 4px solid #e74c3c; padding: 15px 20px; margin: 15px 0; }}
    .signatures {{ border-top: 2px solid #eee; margin-top: 40px; padding-top: 25px; }}
    .sig-box {{ display: inline-block; width: 45%; vertical-align: top; background: #f8f9fa; border-radius: 10px; padding: 20px; text-align: center; margin: 0 2%; }}
    .sig-nom {{ font-family: 'Palatino Linotype', serif; font-size: 1.5rem; font-style: italic; border-bottom: 2px solid #1a1a2e; padding-bottom: 4px; margin: 10px 0; color: #1a1a2e; }}
    .sig-label {{ font-size: 0.75rem; color: #888; font-weight: 700; margin-bottom: 10px; }}
    .sig-detail {{ font-size: 0.75rem; color: #666; }}
    .badge-signe {{ background: #27ae60; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-top: 8px; }}
    .footer {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #eee; font-size: 0.75rem; color: #999; text-align: center; }}
  </style>
</head>
<body>

  <div class="header">
    <p style="letter-spacing:3px;font-size:0.8rem;color:#f0a500;font-weight:600;">DOCUMENT OFFICIEL — ARCHIVÉ</p>
    <h1>TontineSecure</h1>
    <p>Société de gestion de tontines sécurisées</p>
    <div class="badge-contrat">CONTRAT DE PARTICIPATION À UNE TONTINE</div>
  </div>

  <div class="meta">
    <table>
      <tr><td>RÉFÉRENCE CONTRAT</td><td><strong>{reference_contrat}</strong></td></tr>
      <tr><td>TONTINE</td><td><strong>{tontine.code}</strong></td></tr>
      <tr><td>PARTICIPANT</td><td><strong>{membre_nom}</strong></td></tr>
      <tr><td>EMAIL</td><td>{membre_email}</td></tr>
      <tr><td>DATE DE SIGNATURE</td><td><strong>{date_signature}</strong></td></tr>
      <tr><td>ADRESSE IP</td><td>{ip_signature}</td></tr>
      <tr><td>COTISATION MENSUELLE</td><td><strong>{tontine.montant_panier:,.0f} FCFA</strong></td></tr>
      <tr><td>PANIER TOTAL MENSUEL</td><td><strong>{tontine.montant_panier * tontine.max_membres:,.0f} FCFA</strong></td></tr>
      <tr><td>DURÉE TOTALE</td><td><strong>{tontine.max_membres} mois</strong></td></tr>
    </table>
  </div>

  <h2>Article 1 — Parties au contrat</h2>
  <p>Le présent contrat est conclu entre <strong>TontineSecure</strong>, société de gestion de tontines sécurisées,
  ci-après dénommée « l'Organisateur », et <strong>{membre_nom}</strong>,
  ci-après dénommé « le Participant », dont l'identité a été vérifiée par procédure KYC sur la plateforme TontineSecure.</p>
  <p>Le Participant reconnaît avoir pris connaissance des conditions générales de la plateforme
  et accepte sans réserve les termes du présent contrat.</p>

  <h2>Article 2 — Objet du contrat</h2>
  <p>Le présent contrat a pour objet la participation du Participant à une tontine anonyme et sécurisée
  organisée par TontineSecure. Un groupe de participants cotise mensuellement un montant fixe.
  Chaque mois, la totalité des cotisations collectées est versée à l'un des membres du groupe,
  selon un ordre de passage établi et confidentiel.</p>

  <h2>Article 3 — Anonymat et confidentialité</h2>
  <p>TontineSecure garantit l'anonymat total entre les membres du groupe. Aucun Participant
  n'a accès à l'identité des autres membres. Seul l'Organisateur connaît l'identité de chaque Participant
  dans le cadre de la procédure de vérification KYC et de la gestion des obligations contractuelles.</p>
  <p>Le Participant s'engage à ne pas tenter d'identifier les autres membres et à respecter
  la confidentialité absolue de la tontine. Toute violation entraîne la résiliation immédiate du contrat.</p>

  <h2>Article 4 — Garantie de paiement par TontineSecure</h2>
  <div class="garantie">
    <strong style="color:#27ae60;">✅ GARANTIE ABSOLUE DE PAIEMENT</strong><br><br>
    TontineSecure s'engage formellement et irrévocablement à verser le panier mensuel
    au Participant désigné, <strong>même en cas de défaillance d'un ou plusieurs membres</strong>
    du groupe. TontineSecure avancera les fonds manquants et se chargera elle-même
    du recouvrement auprès du membre défaillant.
  </div>

  <h2>Article 5 — Obligations du Participant</h2>
  <p>Le Participant s'engage à :</p>
  <ol>
    <li>Maintenir un solde suffisant sur son compte TontineSecure pour permettre le prélèvement automatique le 5 de chaque mois.</li>
    <li>Recharger son compte au plus tard le <strong>4 du mois</strong> en cours.</li>
    <li>Fournir des informations exactes et à jour lors de la procédure KYC.</li>
    <li>Respecter la confidentialité et l'anonymat des autres membres.</li>
    <li>Honorer ses engagements financiers pour la durée totale de la tontine ({tontine.max_membres} mois).</li>
  </ol>

  <h2>Article 6 — Pénalités de retard</h2>
  <div class="penalite">
    <strong style="color:#e74c3c;">⚠️ PÉNALITÉS APPLICABLES</strong>
    <ul>
      <li>Tout retard de paiement au-delà du <strong>9 du mois</strong> entraîne automatiquement une pénalité de <strong>1,5 % du montant de la cotisation due</strong>.</li>
      <li>Cette pénalité est due pour chaque mois de retard et s'accumule jusqu'à régularisation.</li>
      <li>Le Participant reçoit une notification de mise en demeure dès le premier jour de retard.</li>
      <li>Les pénalités sont prélevées automatiquement lors de la régularisation du solde.</li>
    </ul>
  </div>
  <p>Exemple : Pour une cotisation de {tontine.montant_panier:,.0f} FCFA, la pénalité mensuelle est de <strong>{tontine.montant_panier * 0.015:,.0f} FCFA</strong>.</p>

  <h2>Article 7 — Procédures en cas d'impayé prolongé</h2>
  <div class="escalade">
    <strong style="color:#e74c3c;">Procédure d'escalade en cas de non-paiement :</strong>
    <ol>
      <li><strong>Mois 1 de retard :</strong> Notification d'alerte + pénalité 1,5 % applicable le 9 du mois.</li>
      <li><strong>Mois 2 de retard :</strong> Mise en demeure officielle + pénalité cumulée + suspension temporaire.</li>
      <li><strong>Mois 3 de retard et au-delà :</strong> TontineSecure se réserve le droit d'engager toutes poursuites judiciaires nécessaires au recouvrement des sommes dues, incluant le principal, les pénalités, et les frais de procédure, conformément au droit OHADA en vigueur.</li>
    </ol>
  </div>
  <p>Le Participant reconnaît expressément que TontineSecure dispose d'un droit de recouvrement
  sur toute somme due et non payée, et que les informations KYC fournies pourront être utilisées
  dans le cadre de procédures de recouvrement judiciaire ou amiable.</p>

  <h2>Article 8 — Résiliation et exclusion</h2>
  <p>TontineSecure se réserve le droit de résilier le présent contrat et d'exclure le Participant
  en cas de : fraude avérée, usurpation d'identité, violation de la confidentialité,
  ou non-paiement persistant au-delà de 3 mois. En cas d'exclusion, le Participant reste
  redevable de toutes les sommes dues, majorées des pénalités et frais de procédure.</p>

  <h2>Article 9 — Protection des données personnelles</h2>
  <p>TontineSecure s'engage à protéger les données personnelles du Participant conformément
  aux législations en vigueur. Les informations collectées sont utilisées exclusivement pour
  la gestion de la tontine, la vérification d'identité, et le cas échéant, les procédures de recouvrement.</p>

  <h2>Article 10 — Droit applicable et juridiction</h2>
  <p>Le présent contrat est régi par le droit OHADA et les législations nationales applicables
  en République du Sénégal et en République de Côte d'Ivoire. Tout litige sera soumis aux
  juridictions compétentes du lieu du siège social de TontineSecure.</p>

  <div class="signatures">
    <div class="sig-box">
      <div class="sig-label">SIGNATURE DE L'ORGANISATEUR</div>
      <div class="sig-nom">TontineSecure</div>
      <div class="sig-detail">Direction Générale — TontineSecure SARL</div>
      <div class="badge-signe">✅ SIGNÉ ÉLECTRONIQUEMENT</div>
    </div>
    <div class="sig-box">
      <div class="sig-label">SIGNATURE DU PARTICIPANT</div>
      <div class="sig-nom">{membre_nom}</div>
      <div class="sig-detail">{membre_email}</div>
      <div class="sig-detail">IP : {ip_signature}</div>
      <div class="badge-signe">✅ SIGNÉ LE {date_signature}</div>
    </div>
  </div>

  <div class="footer">
    <p>Document archivé par TontineSecure — Référence : {reference_contrat} — Hash d'intégrité disponible sur demande.</p>
    <p>Ce contrat a été signé électroniquement et a la même valeur juridique qu'un contrat manuscrit conformément au droit OHADA.</p>
  </div>

</body>
</html>\"\"\"
"""

# Injecter la fonction avant les routes
content = content.replace(
    "@contrats.route",
    nouvelle_logique + "\n@contrats.route",
    1
)

# Mettre a jour signer_contrat pour stocker le HTML
ancien = """    contrat_existant.hash_contrat = secrets.token_hex(32)"""
nouveau = """    contrat_existant.hash_contrat = secrets.token_hex(32)
    contrat_existant.contenu_html = generer_contenu_html(
        membre_nom=profil.nom_complet if profil else current_user.email,
        membre_email=current_user.email,
        tontine=tontine,
        reference_contrat=contrat_existant.reference,
        ip_signature=request.remote_addr,
        date_signature=datetime.utcnow().strftime("%d/%m/%Y à %H:%M")
    )"""

content = content.replace(ancien, nouveau)
open("app/contrats/__init__.py", "w", encoding="utf-8").write(content)
print("OK stockage HTML contrat!")
