content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

# Verifier combien d articles il y a dans le template HTML
import re
articles = re.findall(r'Article \d+', content)
print("Articles dans le TEMPLATE contrat.html :")
for a in set(articles):
    print(" -", a)
print(f"\nTotal unique : {len(set(articles))}")
print("\nArticle 10 frais present :", "Frais de service" in content)
print("Article 11 fonds garantie present :", "Fonds de garantie et conditions" in content)
print("Article 12 droit applicable present :", "Article 12" in content)
