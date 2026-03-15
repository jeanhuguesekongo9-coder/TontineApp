content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()
print("=== FIN DU FICHIER ===")
print(content[-3000:])
