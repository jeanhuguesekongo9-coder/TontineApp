content = open("app/templates/paiements/dashboard.html", encoding="utf-8-sig", errors="replace").read()

# Remplacer les filtres format(',d') qui cassent Jinja2
content = content.replace(
    "{{ transactions|selectattr('sens','eq','credit')|sum(attribute='montant')|int|format(',d') }} FCFA",
    "{{ '%s'|format(transactions|selectattr('sens','eq','credit')|sum(attribute='montant')|int) }} FCFA"
)
content = content.replace(
    "{{ transactions|selectattr('sens','eq','debit')|sum(attribute='montant')|int|format(',d') }} FCFA",
    "{{ '%s'|format(transactions|selectattr('sens','eq','debit')|sum(attribute='montant')|int) }} FCFA"
)

open("app/templates/paiements/dashboard.html", "w", encoding="utf-8").write(content)
print("OK!")
