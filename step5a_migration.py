import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'
from app import create_app
app = create_app('development')
with app.app_context():
    from app.models import db
    db.create_all()
    print("OK! Tables creees/mises a jour")
    from app.models import Penalite
    print("OK! Modele Penalite accessible")
