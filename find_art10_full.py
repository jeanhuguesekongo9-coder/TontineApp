import re
content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Trouver et remplacer tout le bloc Article 10 dans le template
ancien = re.search(r'<div style="margin-bottom:30px;">\s*<h5[^>]*>\s*Article 10.*?</div>\s*</div>', content, re.DOTALL)
if ancien:
    print("Trouve! Longueur:", len(ancien.group()))
    print("Debut:", ancien.group()[:100])
else:
    # Chercher autrement
    idx = content.find("Article 10")
    print("Position Article 10:", idx)
    print("Contexte complet:")
    print(content[idx-200:idx+500])
