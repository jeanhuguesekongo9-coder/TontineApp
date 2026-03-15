content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()

# Remplacer l'ancien Article 10 (droit applicable) par les 3 nouveaux articles
ancien_art10 = """  <h2>Article 10 — Droit applicable et juridiction</h2>
  <p>Le présent contrat est régi par le droit OHADA et les législations nationales applicables
  en République du Sénégal et en République de Côte d'Ivoire. Tout litige sera soumis aux
  juridictions compétentes du lieu du siège social de TontineSecure.</p>

  <div class="signatures">"""

nouveau_arts = """  <h2>Article 10 — Frais de service TontineSecure</h2>
  <p>En contrepartie des services rendus par TontineSecure (gestion, sécurisation, traçabilité et garantie conditionnelle), les frais suivants s'appliquent :</p>
  <ul style="line-height:2.2;">
    <li>
      <strong>Frais sur chaque recharge — taux total de 1,5 % :</strong>
      À chaque recharge effectuée par le Participant, des frais de 1,5 % sont automatiquement
      prélevés sur le montant brut rechargé et se décomposent comme suit :
      <ul style="margin-top:8px;line-height:2.2;">
        <li>
          <strong>0,5 % → Fonds de garantie de la tontine :</strong>
          Cette portion est exclusivement affectée au fonds de garantie collectif de la tontine
          à laquelle appartient le Participant. Ce fonds, constitué progressivement par les
          contributions de tous les membres, a pour unique vocation de couvrir les défaillances
          de paiement au sein du groupe. Il appartient collectivement aux membres de la tontine
          et est géré en fiducie par TontineSecure. Lorsque ce fonds atteint le seuil d'activation
          de 20 % du panier mensuel, TontineSecure peut avancer les sommes dues en cas de
          non-paiement d'un membre, garantissant ainsi à chaque Participant la réception de son
          panier à la date prévue.
        </li>
        <li>
          <strong>1 % → Revenus de gestion TontineSecure :</strong>
          Cette portion constitue la rémunération de TontineSecure pour l'ensemble des services
          rendus aux membres, notamment : la gestion et la sécurisation des fonds, la vérification
          KYC des membres, l'archivage permanent et inaltérable des contrats, la mise à disposition
          de la plateforme numérique, le traitement des paiements, la gestion des pénalités et des
          procédures de recouvrement, ainsi que le support client.
        </li>
      </ul>
      <div style="background:#f0f8ff;border-left:3px solid #1DC8EE;padding:10px 15px;margin-top:10px;border-radius:0 6px 6px 0;">
        <strong>Exemple concret :</strong> Pour une recharge de 100 000 FCFA, les frais s'élèvent
        à 1 500 FCFA. Le Participant reçoit sur son solde 98 500 FCFA nets. Sur les 1 500 FCFA
        de frais : 500 FCFA sont affectés au fonds de garantie de sa tontine et 1 000 FCFA
        constituent les revenus de TontineSecure.
      </div>
    </li>
    <li style="margin-top:15px;">
      <strong>Frais annuels de tenue de compte — 1 % du panier mensuel :</strong>
      Chaque année civile (prélevés automatiquement le 1er janvier), des frais de tenue de compte
      s'élevant à 1 % du montant du panier mensuel de la tontine sont débités sur le solde du
      Participant. Ces frais couvrent spécifiquement les charges suivantes :
      <ul style="margin-top:8px;line-height:2.2;">
        <li>L'archivage sécurisé et permanent du contrat signé électroniquement ;</li>
        <li>La maintenance et l'hébergement de la plateforme TontineSecure ;</li>
        <li>La gestion administrative du dossier du Participant ;</li>
        <li>La conservation des preuves de paiement et des historiques de transactions ;</li>
        <li>Les coûts liés à la conformité réglementaire et juridique.</li>
      </ul>
      <div style="background:#f0f8ff;border-left:3px solid #1DC8EE;padding:10px 15px;margin-top:10px;border-radius:0 6px 6px 0;">
        <strong>Exemple concret :</strong> Pour une tontine dont le panier mensuel est de
        {tontine.montant_panier:,.0f} FCFA, les frais annuels de tenue de compte s'élèvent à
        <strong>{tontine.montant_panier * 0.01:,.0f} FCFA par an</strong>,
        soit environ <strong>{tontine.montant_panier * 0.01 / 12:,.0f} FCFA par mois</strong>.
      </div>
    </li>
    <li style="margin-top:15px;">
      <strong>Pénalités de retard — 1,5 % par mois de retard :</strong>
      Telles que définies à l'Article 6, les pénalités de retard sont intégralement perçues par
      TontineSecure en compensation du préjudice causé au groupe et des frais de gestion du
      recouvrement engagés.
    </li>
  </ul>
  <p>Le Participant reconnaît avoir été informé de l'ensemble de ces frais et les accepte
  expressément en signant le présent contrat.</p>

  <h2>Article 11 — Fonds de garantie et conditions d'activation</h2>
  <p>TontineSecure constitue, pour chaque tontine, un fonds de garantie collectif alimenté
  exclusivement par la part de 0,5 % prélevée sur chaque recharge des membres.</p>
  <p><strong>La garantie de paiement décrite à l'Article 4 n'est activée que lorsque le fonds
  de garantie de la tontine atteint un seuil minimum de 20 % du panier mensuel total</strong>,
  soit <strong>{tontine.montant_panier * tontine.max_membres * 0.20:,.0f} FCFA</strong>
  pour la présente tontine ({tontine.code}).</p>
  <p>Avant l'atteinte de ce seuil, TontineSecure met en œuvre tous les moyens contractuels,
  juridiques et de recouvrement à sa disposition pour assurer le paiement des membres, sans
  engagement de substitution financière directe de sa part.</p>
  <p>Une fois le seuil atteint et le fonds activé, TontineSecure s'engage à avancer les sommes
  dues en cas de défaillance d'un membre et à procéder au recouvrement intégral auprès du
  membre défaillant, y compris par voie judiciaire si nécessaire.</p>
  <p>Le Participant sera notifié par la plateforme lorsque le fonds de garantie de sa tontine
  aura atteint son seuil d'activation.</p>

  <h2>Article 12 — Droit applicable et juridiction</h2>
  <p>Le présent contrat est régi par le droit OHADA et les législations nationales applicables
  en République du Sénégal et en République de Côte d'Ivoire. Tout litige relatif à
  l'interprétation ou à l'exécution du présent contrat sera soumis aux juridictions compétentes
  du lieu du siège social de TontineSecure.</p>

  <div class="signatures">"""

content = content.replace(ancien_art10, nouveau_arts)
open("app/contrats/__init__.py", "w", encoding="utf-8").write(content)

# Verifier
import re
articles = re.findall(r'<h2>Article \d+', content)
print("Articles dans le contrat :")
for a in articles:
    print(" -", a)
