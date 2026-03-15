content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()
idx = content.find("signatures")
if idx >= 0:
    print(content[idx-100:idx+1500])
