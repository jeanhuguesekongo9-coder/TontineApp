content = open("app/templates/admin/kyc.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    '<a href="/uploads/{{ k.doc_identite }}" target="_blank"',
    '<a href="{{ url_for(\'admin.voir_fichier\', chemin=k.doc_identite) }}" target="_blank"'
)
open("app/templates/admin/kyc.html", "w", encoding="utf-8").write(content)
print("OK!")
