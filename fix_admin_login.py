content = open("app/auth/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    "        if not user.profil:\n            return redirect(url_for(\"auth.completer_profil\"))\n        if not user.tel_verifie:\n            return redirect(url_for(\"auth.verifier_telephone\"))\n        if not user.kyc_valide:\n            return redirect(url_for(\"kyc.soumettre\"))\n        return redirect(url_for(\"main.tableau_de_bord\"))",
    "        if user.role == \"admin\":\n            return redirect(url_for(\"admin.dashboard\"))\n        if not user.profil:\n            return redirect(url_for(\"auth.completer_profil\"))\n        if not user.tel_verifie:\n            return redirect(url_for(\"auth.verifier_telephone\"))\n        if not user.kyc_valide:\n            return redirect(url_for(\"kyc.soumettre\"))\n        return redirect(url_for(\"main.tableau_de_bord\"))"
)
open("app/auth/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
