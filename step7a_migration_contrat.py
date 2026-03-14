import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'

# Ajouter colonne contenu_html dans le modele Contrat
content = open("app/models.py", encoding="utf-8-sig", errors="replace").read()
if "contenu_html" not in content:
    content = content.replace(
        "    hash_contrat = db.Column(db.String(64))",
        "    hash_contrat = db.Column(db.String(64))\n    contenu_html = db.Column(db.Text)"
    )
    open("app/models.py", "w", encoding="utf-8").write(content)
    print("OK colonne contenu_html ajoutée dans Contrat!")
else:
    print("Déjà présent!")

from app import create_app
app = create_app('development')
with app.app_context():
    from app.models import db
    db.create_all()
    print("OK! Migration BDD réussie — colonne contenu_html créée")
