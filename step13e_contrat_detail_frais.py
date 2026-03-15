content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()

ancien = """    <li><strong>Frais sur chaque recharge (1,5 %) :</strong> À chaque recharge effectuée par le Participant, des frais de 1,5 % sont prélevés sur le montant brut rechargé. Ces frais sont décomposés comme suit : 0,5 % est affecté au fonds de garantie de la tontine et 1 % constitue les revenus de TontineSecure pour la gestion du service.</li>
    <li><strong>Frais annuels de tenue de compte (1 %) :</strong> Chaque année, des frais de tenue de compte s'élevant à 1 % du montant du panier mensuel de la tontine sont prélevés automatiquement sur le solde du Participant. Ces frais couvrent les coûts d'archivage, de maintenance de la plateforme et de gestion administrative.</li>
    <li><strong>Pénalités de retard (1,5 %/mois) :</strong> Telles que définies à l'Article 6, les pénalités de retard sont intégralement perçues par TontineSecure.</li>"""

nouveau = """    <li>
      <strong>Frais sur chaque recharge — taux total de 1,5 % :</strong>
      À chaque recharge effectuée par le Participant sur la plateforme TontineSecure,
      des frais de 1,5 % sont automatiquement prélevés sur le montant brut rechargé.
      Ces frais sont décomposés de la manière suivante :
      <ul style="margin-top:8px;line-height:2.2;">
        <li>
          <strong>0,5 % → Fonds de garantie de la tontine :</strong>
          Cette portion est exclusivement affectée au fonds de garantie collectif
          de la tontine à laquelle appartient le Participant. Ce fonds, constitué
          progressivement par les contributions de tous les membres, a pour unique
          vocation de couvrir les défaillances de paiement au sein du groupe.
          Lorsque ce fonds atteint le seuil d'activation de 20 % du panier mensuel,
          TontineSecure peut avancer les sommes dues en cas de non-paiement d'un membre,
          garantissant ainsi à chaque Participant la réception de son panier à la date prévue.
          Ce fonds appartient collectivement aux membres de la tontine et est géré
          en fiducie par TontineSecure.
        </li>
        <li>
          <strong>1 % → Revenus de gestion TontineSecure :</strong>
          Cette portion constitue la rémunération de TontineSecure pour l'ensemble
          des services rendus aux membres, notamment : la gestion et la sécurisation
          des fonds, la vérification KYC des membres, l'archivage permanent et
          inaltérable des contrats, la mise à disposition de la plateforme numérique,
          le traitement des paiements, la gestion des pénalités et des procédures
          de recouvrement, ainsi que le support client.
        </li>
      </ul>
      <div style="background:#f0f8ff;border-left:3px solid #1DC8EE;padding:10px 15px;margin-top:10px;border-radius:0 6px 6px 0;">
        <strong>Exemple concret :</strong> Pour une recharge de 100 000 FCFA,
        les frais s'élèvent à 1 500 FCFA. Le Participant reçoit sur son solde
        98 500 FCFA nets. Sur les 1 500 FCFA de frais : 500 FCFA vont au fonds
        de garantie de sa tontine et 1 000 FCFA constituent les revenus de
        TontineSecure.
      </div>
    </li>
    <li style="margin-top:15px;">
      <strong>Frais annuels de tenue de compte — 1 % du panier mensuel :</strong>
      Chaque année civile (prélevés le 1er janvier), des frais de tenue de compte
      s'élevant à 1 % du montant du panier mensuel de la tontine sont prélevés
      automatiquement sur le solde du Participant.
      Ces frais couvrent les charges suivantes :
      <ul style="margin-top:8px;line-height:2.2;">
        <li>L'archivage sécurisé et permanent du contrat signé électroniquement ;</li>
        <li>La maintenance et l'hébergement de la plateforme TontineSecure ;</li>
        <li>La gestion administrative du dossier du Participant ;</li>
        <li>La conservation des preuves de paiement et des historiques de transactions ;</li>
        <li>Les coûts liés à la conformité réglementaire et juridique.</li>
      </ul>
      <div style="background:#f0f8ff;border-left:3px solid #1DC8EE;padding:10px 15px;margin-top:10px;border-radius:0 6px 6px 0;">
        <strong>Exemple concret :</strong> Pour une tontine dont le panier mensuel
        est de {tontine.montant_panier:,.0f} FCFA, les frais annuels de tenue de compte
        s'élèvent à <strong>{tontine.montant_panier * 0.01:,.0f} FCFA par an</strong>,
        soit environ <strong>{tontine.montant_panier * 0.01 / 12:,.0f} FCFA par mois</strong>.
      </div>
    </li>
    <li style="margin-top:15px;">
      <strong>Pénalités de retard — 1,5 % par mois de retard :</strong>
      Telles que définies à l'Article 6, les pénalités de retard sont intégralement
      perçues par TontineSecure en compensation du préjudice causé au groupe et
      des frais de gestion du recouvrement engagés.
    </li>"""

content = content.replace(ancien, nouveau)
open("app/contrats/__init__.py", "w", encoding="utf-8").write(content)
print("OK article 10 détaillé avec explication complète des frais!")
