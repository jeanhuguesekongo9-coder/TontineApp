content = open("app/admin/__init__.py", encoding="utf-8-sig", errors="replace").read()

# Supprimer l'ancienne route voir_fichier peu importe son contenu
import re
content = re.sub(
    r'@admin\.route\("/fichier/<path:chemin>"\).*?def voir_fichier\(chemin\):.*?(?=\n@admin|\Z)',
    '''@admin.route("/fichier/<path:chemin>")
@admin_requis
def voir_fichier(chemin):
    import os
    from supabase import create_client
    from flask import redirect
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(url, key)
    result = client.storage.from_("kyc-documents").create_signed_url(chemin, 300)
    return redirect(result["signedURL"])

''',
    content,
    flags=re.DOTALL
)
open("app/admin/__init__.py", "w", encoding="utf-8").write(content)
print("Admin OK!")
