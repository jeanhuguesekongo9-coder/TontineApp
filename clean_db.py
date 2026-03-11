import os
os.environ["DATABASE_URL"] = "postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
from app import create_app
from app.models import db
app = create_app("development")
with app.app_context():
    db.session.execute(db.text("DELETE FROM membres_tontines WHERE user_id != 1"))
    db.session.execute(db.text("DELETE FROM audit_logs WHERE user_id != 1"))
    db.session.execute(db.text("DELETE FROM notifications WHERE user_id != 1"))
    db.session.execute(db.text("DELETE FROM paiements WHERE user_id != 1"))
    db.session.execute(db.text("DELETE FROM kyc WHERE user_id != 1"))
    db.session.execute(db.text("DELETE FROM profils WHERE user_id != 1"))
    db.session.execute(db.text("DELETE FROM utilisateurs WHERE role = 'membre'"))
    db.session.commit()
    count = db.session.execute(db.text("SELECT COUNT(*) FROM utilisateurs")).scalar()
    print("Tout nettoye! Restants:", count)
