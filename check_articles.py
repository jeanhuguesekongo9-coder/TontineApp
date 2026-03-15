content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()

# Verifier ce qui existe dans le contrat
import re
articles = re.findall(r'<h2>Article \d+', content)
print("Articles trouvés dans le contrat :")
for a in articles:
    print(" -", a)
