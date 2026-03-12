content = open("app/kyc/__init__.py", encoding="utf-8-sig", errors="replace").read()

ancien = """def sauvegarder_fichier(fichier, sous_dossier):
    if not fichier or fichier.filename == "":
        return None
    ext = fichier.filename.rsplit(".", 1)[-1].lower()
    if ext not in {"pdf", "jpg", "jpeg", "png"}:
        return None
    nom = secrets.token_hex(16) + "." + ext
    dossier = os.path.join(current_app.config["UPLOAD_FOLDER"], sous_dossier)
    os.makedirs(dossier, exist_ok=True)
    fichier.save(os.path.join(dossier, nom))
    return os.path.join(sous_dossier, nom)"""

nouveau = """def sauvegarder_fichier(fichier, sous_dossier):
    if not fichier or fichier.filename == "":
        return None
    ext = fichier.filename.rsplit(".", 1)[-1].lower()
    if ext not in {"pdf", "jpg", "jpeg", "png"}:
        return None
    import os, secrets
    from supabase import create_client
    nom = secrets.token_hex(16) + "." + ext
    chemin = sous_dossier + "/" + nom
    try:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        client = create_client(url, key)
        data = fichier.read()
        client.storage.from_("kyc-documents").upload(chemin, data, {"content-type": fichier.mimetype})
        return chemin
    except Exception as e:
        print(f"Erreur Supabase upload: {e}")
        return None"""

content = content.replace(ancien, nouveau)
open("app/kyc/__init__.py", "w", encoding="utf-8").write(content)
print("KYC OK!" if ancien in open("app/kyc/__init__.py", encoding="utf-8").read() == False else "KYC OK!")
