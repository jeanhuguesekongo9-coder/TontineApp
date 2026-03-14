import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'
from app import create_app
app = create_app('development')
app.config['TESTING'] = True
app.config['LOGIN_DISABLED'] = True
with app.test_client() as c:
    with app.app_context():
        from app.models import Utilisateur
        admin = Utilisateur.query.filter_by(role='admin').first()
        print('Admin :', admin.email)
        with c.session_transaction() as sess:
            sess['_user_id'] = str(admin.id)
            sess['_fresh'] = True
            sess['user_id'] = admin.id
        r7  = c.get('/admin/tableau-de-bord')
        r8  = c.get('/admin/penalites')
        r9  = c.get('/admin/soldes')
        r10 = c.get('/admin/recharges')
        r11 = c.get('/admin/contrats')
        print('Tableau de bord admin :', r7.status_code)
        print('Pénalités admin :', r8.status_code)
        print('Soldes admin :', r9.status_code)
        print('Recharges admin :', r10.status_code)
        print('Contrats admin :', r11.status_code)
        for label, r in [('tableau', r7), ('penalites', r8), ('contrats', r11)]:
            if r.status_code == 500:
                print(f'ERREUR {label} :', r.data.decode('utf-8')[:300])
