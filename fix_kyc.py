content = open("app/templates/kyc/soumettre.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    'Bulletin de salaire (3 derniers mois) <span style="color:#e74c3c;">*</span>',
    'Bulletin de salaire (3 derniers mois) <span class="text-muted" style="font-size:0.85rem;">(optionnel)</span>'
)
content = content.replace(
    'accept=".pdf,.jpg,.jpeg,.png" required>',
    'accept=".pdf,.jpg,.jpeg,.png">'
)
content = content.replace(
    'Photo de profil (optionnel)</label>',
    'Photo de profil <span style="color:#e74c3c;">*</span></label>'
)
content = content.replace(
    'name="photo_profil" class="form-control" accept=".jpg,.jpeg,.png">',
    'name="photo_profil" class="form-control" accept=".jpg,.jpeg,.png" required>'
)
open("app/templates/kyc/soumettre.html", "w", encoding="utf-8").write(content)
print("OK!")
