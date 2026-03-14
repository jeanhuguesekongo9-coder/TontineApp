content = open("app/templates/paiements/recharger.html", encoding="utf-8-sig", errors="replace").read()
if "/static/logos/wave.svg" in content:
    print("OK - Logo Wave trouve dans le template!")
else:
    print("ERREUR - Logo Wave PAS trouve!")
if "/static/logos/orange.svg" in content:
    print("OK - Logo Orange trouve!")
else:
    print("ERREUR - Logo Orange PAS trouve!")
if "/static/logos/mtn.svg" in content:
    print("OK - Logo MTN trouve!")
else:
    print("ERREUR - Logo MTN PAS trouve!")
