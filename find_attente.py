content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()
idx = content.find("En attente de votre signature")
if idx >= 0:
    print("Trouve:")
    print(content[idx-500:idx+200])
else:
    print("NON TROUVE")
