content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Trouver la zone signatures actuelle et la remplacer
import re
idx = content.find("<!-- Signatures -->")
if idx < 0:
    idx = content.find("display:grid;grid-template-columns:1fr 1fr")
    
print("Position zone signatures:", idx)
print("Contexte:", content[idx-50:idx+200] if idx >= 0 else "NON TROUVE")
