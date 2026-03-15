content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()
idx = content.find("check1")
if idx >= 0:
    print("Zone signature trouvee:")
    print(content[idx-200:idx+800])
else:
    print("Zone signature NON trouvee!")
