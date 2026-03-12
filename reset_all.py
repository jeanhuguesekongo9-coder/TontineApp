import os
os.environ["DATABASE_URL"] = "postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
from app import create_app
from app.models import db
app = create_app("development")
with app.app_context():
    db.session.execute(db.text("DELETE FROM membres_tontines"))
    db.session.execute(db.text("DELETE FROM audit_logs"))
    db.session.execute(db.text("DELETE FROM notifications"))
    db.session.execute(db.text("DELETE FROM paiements"))
    db.session.execute(db.text("DELETE FROM kyc"))
    db.session.execute(db.text("DELETE FROM profils"))
    db.session.execute(db.text("DELETE FROM tontines"))
    db.session.execute(db.text("DELETE FROM utilisateurs WHERE role = 'membre'"))
    db.session.execute(db.text("ALTER SEQUENCE utilisateurs_id_seq RESTART WITH 2"))
    db.session.execute(db.text("ALTER SEQUENCE profils_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE audit_logs_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE notifications_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE paiements_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE kyc_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE membres_tontines_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE tontines_id_seq RESTART WITH 1"))
    db.session.commit()
    print("Tout nettoye! Base remise a zero.")
