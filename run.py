# -*- coding: utf-8 -*-
from app import create_app
from app.models import db, Utilisateur
from flask import send_from_directory
import os

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Utilisateur=Utilisateur)

@app.cli.command()
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de donnees initialisee")

@app.cli.command()
def creer_admin():
    with app.app_context():
        from app.models import Profil
        from datetime import date
        email = 'admin@tontinesecure.com'
        mdp = 'Admin@2025!'
        if Utilisateur.query.filter_by(email=email).first():
            print(f"Admin {email} existe deja.")
            return
        admin = Utilisateur(email=email, role='admin')
        admin.set_password(mdp)
        admin.email_verifie = True
        admin.tel_verifie = True
        admin.kyc_valide = True
        admin.compte_actif = True
        db.session.add(admin)
        db.session.flush()
        profil = Profil(user_id=admin.id, nom='Admin', prenom='TontineSecure',
            date_naissance=date(1990,1,1), telephone='+00000000000',
            ville='Paris', pays='France', profession='Administrateur')
        db.session.add(profil)
        db.session.commit()
        print(f"Admin cree : {email} / {mdp}")

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    return send_from_directory(upload_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

