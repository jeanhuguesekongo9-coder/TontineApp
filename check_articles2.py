import re
content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()
articles = re.findall(r'<h2>Article \d+', content)
print(f"Nombre d articles dans le code : {len(articles)}")
for a in articles:
    print(" -", a)
