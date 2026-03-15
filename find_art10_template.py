content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Remplacer l'article 10 dans le template HTML
ancien = """      <div style="margin-bottom:30px;">
        <h5 style="color:#1a1a2e;font-family:Playfair Display,serif;border-bottom:2px solid #f0a500;padding-bottom:8px;">
          Article 10 — Droit applicable et juridiction
        </h5>
        <p style="color:#444;line-height:1.8;text-align:justify;">
          Le présent contrat est régi par le droit OHADA et les législations nationales applicables
          en République du Sénégal et en République de Côte d'Ivoire. Tout litige relatif à
          l'interprétation ou à l'exécution du présent contrat sera soumis aux juridictions
          compétentes du lieu du siège social de TontineSecure.
        </p>
      </div>"""

# Si le remplacement exact ne marche pas, cherchons ce qui existe
import re
match = re.search(r'Article 10.*?</div>', content, re.DOTALL)
if match:
    print("Article 10 trouve dans template:")
    print(match.group()[:200])
else:
    print("Article 10 non trouve avec regex")
    # Chercher autrement
    idx = content.find("Article 10")
    if idx >= 0:
        print("Article 10 trouve à position", idx)
        print("Contexte:", content[idx-50:idx+300])
