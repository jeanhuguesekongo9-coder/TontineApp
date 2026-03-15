import os
os.environ["DATABASE_URL"] = "postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
from app import create_app
app = create_app("development")
app.config["TESTING"] = True
with app.test_client() as c:
    with app.app_context():
        from app.models import Utilisateur
        u = Utilisateur.query.filter_by(role="membre").first()
        print("Membre:", u.email if u else "AUCUN")
        if u:
            with c.session_transaction() as sess:
                sess["_user_id"] = str(u.id)
                sess["_fresh"] = True
            r = c.get("/paiements/")
            print("Status:", r.status_code)
            if r.status_code == 500:
                print("ERREUR:", r.data.decode("utf-8")[:1000])
