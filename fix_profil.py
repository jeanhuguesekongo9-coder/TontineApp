content = open("app/contrats/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    "    contrat_existant.hash_contrat = secrets.token_hex(32)",
    "    profil = Profil.query.filter_by(user_id=current_user.id).first()\n    contrat_existant.hash_contrat = secrets.token_hex(32)"
)
open("app/contrats/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
