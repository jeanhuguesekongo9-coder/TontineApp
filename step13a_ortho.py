import os

# 1. Corriger tontines/__init__.py (caracteres corrompus)
content = open("app/tontines/__init__.py", encoding="utf-8-sig", errors="replace").read()
corrections = {
    "doit \ufffdtre approuv\ufffd": "doit être approuvé",
    "Votre dossier KYC doit \ufffdtre approuv\ufffd\ufffd avant de rejoindre une tontine.": "Votre dossier KYC doit être approuvé avant de rejoindre une tontine.",
    "Cette tontine est compl\ufffd\ufffdde.": "Cette tontine est complète.",
    "Vous \ufffd\ufffdes d\ufffd\ufffd\ufffd\ufffd membre de cette tontine.": "Vous êtes déjà membre de cette tontine.",
    "Ã\xaatre approuvÃ©": "être approuvé",
    "complÃ¨te": "complète",
    "Ã\xaatre dÃ©jÃ ": "être déjà",
}
for ancien, nouveau in corrections.items():
    content = content.replace(ancien, nouveau)
# Réécriture propre des flash messages
content = content.replace(
    'flash("Votre dossier KYC doit \ufffdtre approuv\ufffd\ufffd avant de rejoindre une tontine.", "warning")',
    'flash("Votre dossier KYC doit être approuvé avant de rejoindre une tontine.", "warning")'
)
content = content.replace(
    'flash("Cette tontine est compl\ufffd\ufffdde.", "warning")',
    'flash("Cette tontine est complète.", "warning")'
)
content = content.replace(
    'flash("Vous \ufffd\ufffdes d\ufffd\ufffd\ufffd\ufffd membre de cette tontine.", "info")',
    'flash("Vous êtes déjà membre de cette tontine.", "info")'
)
# Correction avec les vrais caractères corrompus en latin
content = content.replace("Ã\xaatre approuvÃ©", "être approuvé")
content = content.replace("complÃ¨te", "complète")
content = content.replace("Ã\xaatre dÃ©jÃ ", "être déjà")
open("app/tontines/__init__.py", "w", encoding="utf-8").write(content)
print("OK tontines corrigé!")

# 2. Corriger tableau_de_bord.html
content = open("app/templates/admin/tableau_de_bord.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Retardatairees", "Retardataires")
content = content.replace("Poursuites possibless", "Poursuites possibles")
content = content.replace("Voir penalites", "Voir les pénalités")
open("app/templates/admin/tableau_de_bord.html", "w", encoding="utf-8").write(content)
print("OK tableau_de_bord.html corrigé!")

# 3. Corriger navbar base.html
content = open("app/templates/base.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Penaalites", "Pénalités")
content = content.replace("Penalites", "Pénalités")
open("app/templates/base.html", "w", encoding="utf-8").write(content)
print("OK base.html corrigé!")

# 4. Corriger ma_tontine.html
content = open("app/templates/paiements/ma_tontine.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Non defini", "Non défini")
content = content.replace("identites sont confidentielles", "identités sont confidentielles")
content = content.replace("identites sont masquees", "identités sont masquées")
content = content.replace("Pour garantir la confidentialite et la securite de tous les membres, les identites sont masquees.", "Pour garantir la confidentialité et la sécurité de tous les membres, les identités sont masquées.")
content = content.replace("Seule votre position vous est visible.", "Seule votre position vous est visible.")
content = content.replace("Penalites en cours", "Pénalités en cours")
content = content.replace("Recharger maintenant", "Recharger maintenant")
content = content.replace("Vous n etes membre d aucune tontine pour le moment.", "Vous n'êtes membre d'aucune tontine pour le moment.")
open("app/templates/paiements/ma_tontine.html", "w", encoding="utf-8").write(content)
print("OK ma_tontine.html corrigé!")

# 5. Corriger penalites.html admin
content = open("app/templates/admin/penalites.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Retards de cotisation et mises en demeure", "Retards de cotisation et mises en demeure")
content = content.replace("Mises en demeure (3+ mois)", "Mises en demeure (3 mois et plus)")
content = content.replace("Motif de l annulation", "Motif de l'annulation")
content = content.replace("Aucune penalite", "Aucune pénalité")
content = content.replace("statut.replace(\"_\", \" \")", 'statut.replace("_", " ")')
open("app/templates/admin/penalites.html", "w", encoding="utf-8").write(content)
print("OK penalites.html corrigé!")

# 6. Corriger recharges.html admin
content = open("app/templates/admin/recharges.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Validees", "Validées")
content = content.replace("Rejetees", "Rejetées")
content = content.replace("Aucune recharge", "Aucune recharge")
content = content.replace("Valider cette recharge ?", "Valider cette recharge ?")
content = content.replace("Ref. Transaction", "Réf. Transaction")
content = content.replace("Reference", "Référence")
open("app/templates/admin/recharges.html", "w", encoding="utf-8").write(content)
print("OK recharges.html corrigé!")

# 7. Corriger soldes.html admin
content = open("app/templates/admin/soldes.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Vue d ensemble", "Vue d'ensemble")
content = content.replace("Soldes insuffisants (moins de 5 000 FCFA)", "Soldes insuffisants (moins de 5 000 FCFA)")
content = content.replace("Detail par membre", "Détail par membre")
content = content.replace("Derniere mise a jour", "Dernière mise à jour")
open("app/templates/admin/soldes.html", "w", encoding="utf-8").write(content)
print("OK soldes.html corrigé!")

# 8. Corriger dashboard paiements
content = open("app/templates/paiements/dashboard.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace("Mon Portefeuille", "Mon Portefeuille")
content = content.replace("Historique des transactions", "Historique des transactions")
open("app/templates/paiements/dashboard.html", "w", encoding="utf-8").write(content)
print("OK dashboard.html vérifié!")

print("\n✅ Toutes les corrections orthographiques appliquées!")
