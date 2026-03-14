content = open("app/templates/base.html", encoding="utf-8-sig", errors="replace").read()

# Ajouter "Mon Portefeuille" dans la navbar client
content = content.replace(
    '        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'kyc.soumettre\') }}">Mon KYC</a></li>',
    '        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'kyc.soumettre\') }}">Mon KYC</a></li>\n        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'paiements.dashboard\') }}">💰 Mon Portefeuille</a></li>'
)

# Ajouter "Recharges" dans la navbar admin
content = content.replace(
    '        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'admin.utilisateurs\') }}">Utilisateurs</a></li>',
    '        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'admin.utilisateurs\') }}">Utilisateurs</a></li>\n        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'admin.gerer_recharges\') }}">💳 Recharges</a></li>\n        <li class="nav-item"><a class="nav-link" href="{{ url_for(\'admin.gerer_soldes\') }}">💰 Soldes</a></li>'
)

open("app/templates/base.html", "w", encoding="utf-8").write(content)
print("OK!")
