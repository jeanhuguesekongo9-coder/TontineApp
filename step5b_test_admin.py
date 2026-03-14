import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'
from app import create_app
app = create_app('development')
app.config['TESTING'] = True
with app.test_client() as c:
    with app.app_context():
        from app.models import Utilisateur
        admin = Utilisateur.query.filter_by(role='admin').first()
        print('Admin trouve:', admin.email if admin else 'AUCUN')
        with c.session_transaction() as sess:
            sess['_user_id'] = str(admin.id)
            sess['_fresh'] = True
        r4 = c.get('/admin/tableau-de-bord')
        r5 = c.get('/admin/penalites')
        r6 = c.get('/admin/soldes')
        r7 = c.get('/admin/recharges')
        print('Tableau de bord admin:', r4.status_code)
        print('Penalites admin:', r5.status_code)
        print('Soldes admin:', r6.status_code)
        print('Recharges admin:', r7.status_code)
        if r4.status_code == 500:
            print('ERREUR tableau:', r4.data.decode('utf-8')[:500])
        if r5.status_code == 500:
            print('ERREUR penalites:', r5.data.decode('utf-8')[:500])
