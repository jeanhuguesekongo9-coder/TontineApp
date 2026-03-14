import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'
from app import create_app
app = create_app('development')
app.config['TESTING'] = True
with app.test_client() as c:
    with app.app_context():
        from app.models import Utilisateur, Contrat
        u = Utilisateur.query.filter_by(role='membre').first()
        admin = Utilisateur.query.filter_by(role='admin').first()

        with c.session_transaction() as sess:
            sess['_user_id'] = str(u.id)
            sess['_fresh'] = True
        r1 = c.get('/paiements/')
        r2 = c.get('/paiements/recharger')
        r3 = c.get('/paiements/ma-tontine')
        r4 = c.get('/contrats/mes-contrats')
        print('Dashboard membre :', r1.status_code)
        print('Recharger :', r2.status_code)
        print('Ma tontine :', r3.status_code)
        print('Mes contrats :', r4.status_code)
        if r4.status_code == 500:
            print('ERREUR mes contrats :', r4.data.decode('utf-8')[:400])

        contrat = Contrat.query.filter_by(user_id=u.id, signe=True).first()
        if contrat:
            r5 = c.get(f'/contrats/voir/{contrat.reference}')
            r6 = c.get(f'/contrats/telecharger/{contrat.reference}')
            print('Voir contrat archivé :', r5.status_code)
            print('Télécharger contrat :', r6.status_code)
        else:
            print('Voir contrat archivé : PAS DE CONTRAT SIGNÉ (normal)')

        with c.session_transaction() as sess:
            sess['_user_id'] = str(admin.id)
            sess['_fresh'] = True
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
        if r11.status_code == 500:
            print('ERREUR contrats admin :', r11.data.decode('utf-8')[:400])
