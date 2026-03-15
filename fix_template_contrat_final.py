import re
content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Trouver le bloc exact Article 10 dans le template
pattern = r'<div style="margin-bottom:30px;">\s*<h5[^>]*>\s*Article 10.*?</div>\s*</div>'
match = re.search(pattern, content, re.DOTALL)

nouveau_bloc = """      <div style="margin-bottom:30px;">
        <h5 style="color:#1a1a2e;font-family:Playfair Display,serif;border-bottom:2px solid #f0a500;padding-bottom:8px;">
          Article 10 — Frais de service TontineSecure
        </h5>
        <p style="color:#444;line-height:1.8;text-align:justify;">
          En contrepartie des services rendus par TontineSecure, les frais suivants s'appliquent :
        </p>
        <ul style="color:#444;line-height:2.2;">
          <li>
            <strong>Frais sur chaque recharge — taux total de 1,5 % :</strong>
            À chaque recharge, des frais de 1,5 % sont prélevés automatiquement et se décomposent ainsi :
            <ul style="margin-top:8px;line-height:2.2;">
              <li><strong>0,5 % → Fonds de garantie de la tontine :</strong> Cette portion est exclusivement affectée au fonds de garantie collectif de la tontine. Ce fonds, constitué progressivement par les contributions de tous les membres, couvre les défaillances de paiement. Il est géré en fiducie par TontineSecure. Lorsqu'il atteint 20 % du panier mensuel, TontineSecure peut avancer les sommes dues en cas de non-paiement d'un membre.</li>
              <li><strong>1 % → Revenus de gestion TontineSecure :</strong> Cette portion rémunère les services de TontineSecure : gestion et sécurisation des fonds, vérification KYC, archivage des contrats, mise à disposition de la plateforme, traitement des paiements, gestion des pénalités et recouvrement.</li>
            </ul>
            <div style="background:#f0f8ff;border-left:3px solid #1DC8EE;padding:10px 15px;margin-top:10px;border-radius:0 6px 6px 0;">
              <strong>Exemple :</strong> Pour une recharge de 100 000 FCFA, les frais s'élèvent à 1 500 FCFA. Le Participant reçoit 98 500 FCFA nets. Sur les 1 500 FCFA : 500 FCFA vont au fonds de garantie et 1 000 FCFA constituent les revenus de TontineSecure.
            </div>
          </li>
          <li style="margin-top:15px;">
            <strong>Frais annuels de tenue de compte — 1 % du panier mensuel :</strong>
            Prélevés automatiquement le 1er janvier de chaque année. Ces frais couvrent : l'archivage sécurisé du contrat, la maintenance de la plateforme, la gestion administrative du dossier, la conservation des preuves de paiement et les coûts de conformité réglementaire.
          </li>
          <li style="margin-top:15px;">
            <strong>Pénalités de retard — 1,5 % par mois de retard :</strong>
            Telles que définies à l'Article 6, ces pénalités sont intégralement perçues par TontineSecure.
          </li>
        </ul>
        <p style="color:#444;line-height:1.8;margin-top:10px;">Le Participant reconnaît avoir été informé de l'ensemble de ces frais et les accepte expressément.</p>
      </div>

      <div style="margin-bottom:30px;">
        <h5 style="color:#1a1a2e;font-family:Playfair Display,serif;border-bottom:2px solid #f0a500;padding-bottom:8px;">
          Article 11 — Fonds de garantie et conditions d'activation
        </h5>
        <p style="color:#444;line-height:1.8;text-align:justify;">
          TontineSecure constitue pour chaque tontine un fonds de garantie collectif alimenté par la part de 0,5 % prélevée sur chaque recharge des membres.
        </p>
        <p style="color:#444;line-height:1.8;text-align:justify;">
          <strong>La garantie de paiement n'est activée que lorsque ce fonds atteint un seuil minimum de 20 % du panier mensuel total.</strong> Avant ce seuil, TontineSecure met en œuvre tous les moyens contractuels et juridiques pour assurer le paiement, sans engagement de substitution financière directe. Une fois le seuil atteint, TontineSecure s'engage à avancer les sommes dues et à procéder au recouvrement auprès du membre défaillant, y compris par voie judiciaire si nécessaire.
        </p>
      </div>

      <div style="margin-bottom:30px;">
        <h5 style="color:#1a1a2e;font-family:Playfair Display,serif;border-bottom:2px solid #f0a500;padding-bottom:8px;">
          Article 12 — Droit applicable et juridiction
        </h5>
        <p style="color:#444;line-height:1.8;text-align:justify;">
          Le présent contrat est régi par le droit OHADA et les législations nationales applicables en République du Sénégal et en République de Côte d'Ivoire. Tout litige relatif à l'interprétation ou à l'exécution du présent contrat sera soumis aux juridictions compétentes du lieu du siège social de TontineSecure.
        </p>
      </div>"""

if match:
    content = content[:match.start()] + nouveau_bloc + content[match.end():]
    open("app/templates/contrats/contrat.html", "w", encoding="utf-8").write(content)

    # Verification
    articles = re.findall(r'Article \d+', content)
    print(f"Articles dans le template : {sorted(set(articles))}")
    print("Article 11 present :", "Article 11" in content)
    print("Article 12 present :", "Article 12" in content)
    print("OK! Template mis a jour avec 12 articles!")
else:
    print("ERREUR: bloc non trouve!")
