import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'
from app import create_app
app = create_app('development')
with app.app_context():
    from app.models import db
    try:
        db.engine.execute("ALTER TABLE contrats ADD COLUMN IF NOT EXISTS contenu_html TEXT;")
        print("OK! Colonne contenu_html ajoutée dans PostgreSQL!")
    except Exception as e:
        print(f"Méthode 1 échouée: {e}")
        try:
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE contrats ADD COLUMN IF NOT EXISTS contenu_html TEXT;"))
                conn.commit()
                print("OK! Colonne contenu_html ajoutée!")
        except Exception as e2:
            print(f"Méthode 2 échouée: {e2}")
