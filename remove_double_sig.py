content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Supprimer la zone signatures du bas qui est en double
import re
pattern = r'        <!-- Signatures -->\s*<div style="display:grid.*?</div>\s*</div>\s*\n'
match = re.search(pattern, content, re.DOTALL)
if match:
    print("Zone double trouvee, suppression...")
    content = content[:match.start()] + content[match.end():]
    open("app/templates/contrats/contrat.html", "w", encoding="utf-8").write(content)
    print("OK! Zone supprimee!")
else:
    print("Zone non trouvee - verif manuelle")
    idx = content.find("<!-- Signatures -->")
    print("Position:", idx)
    print(content[idx:idx+200] if idx >= 0 else "AUCUNE")
