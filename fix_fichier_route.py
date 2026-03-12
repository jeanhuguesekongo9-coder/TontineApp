import os
from flask import send_from_directory, current_app

# Ajouter dans app/admin/__init__.py
content = open("app/admin/__init__.py", encoding="utf-8-sig", errors="replace").read()

nouvelle_route = '''
@admin.route("/fichier/<path:chemin>")
@admin_requis
def voir_fichier(chemin):
    from flask import current_app, send_from_directory
    import os
    dossier = os.path.join(current_app.root_path, current_app.config.get("UPLOAD_FOLDER", "uploads"))
    return send_from_directory(os.path.abspath(dossier), chemin)
'''

content = content + nouvelle_route
open("app/admin/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
