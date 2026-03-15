import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.izjnrecwbwmuecqtpmai:Jeanhugue200@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'
from app import create_app
app = create_app('development')
with app.app_context():
    from app.models import db, Contrat, Tontine, Profil, Utilisateur
    from app.contrats import generer_contenu_html
    from datetime import datetime

    contrats = Contrat.query.filter_by(signe=True).all()
    print(f"Contrats signés à régénérer : {len(contrats)}")

    for c in contrats:
        tontine = Tontine.query.get(c.tontine_id)
        utilisateur = Utilisateur.query.get(c.user_id)
        profil = Profil.query.filter_by(user_id=c.user_id).first()
        membre_nom = profil.nom_complet if profil else utilisateur.email

        nouveau_html = generer_contenu_html(
            membre_nom=membre_nom,
            membre_email=utilisateur.email,
            tontine=tontine,
            reference_contrat=c.reference,
            ip_signature=c.ip_signature or "N/A",
            date_signature=c.signe_le.strftime("%d/%m/%Y à %H:%M") if c.signe_le else "N/A"
        )
        c.contenu_html = nouveau_html
        print(f"OK régénéré : {c.reference} — {membre_nom}")

    db.session.commit()
    print(f"\n✅ {len(contrats)} contrat(s) régénéré(s) avec les 12 articles !")
