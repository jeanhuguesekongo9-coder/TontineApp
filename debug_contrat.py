import re
content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()
articles = re.findall(r'<h2>Article \d+', content)
print(f"Nombre d articles dans le CODE : {len(articles)}")
for a in articles:
    print(" -", a)

# Verifier si les nouveaux articles sont presents
print("\nArticle 10 frais present :", "Frais de service TontineSecure" in content)
print("Article 11 fonds garantie present :", "Fonds de garantie et conditions" in content)
print("Article 12 droit applicable present :", "Article 12" in content)
