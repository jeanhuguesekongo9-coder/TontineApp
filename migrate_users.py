from app import create_app
from app.models import db, Utilisateur
from flask_bcrypt import Bcrypt

app = create_app("development")
bcrypt = Bcrypt(app)

with app.app_context():
    users = [
        {"id": 2, "email": "jeanhuguesekongo9@gmail.com", "mot_de_passe": "$2b$12$p7M1k7arUQwgHe1VPHaly.8qIUIEu0Knt0Z6P1RLSzOJNkHIsugrC", "role": "membre"},
        {"id": 3, "email": "jeanhuguesekongo9@yahoo.com", "mot_de_passe": "$2b$12$RI1S43CD7yyoH24Pbtjf/OgjaiphyhCWTnmUEzH3XmZ2fna9OhOi6", "role": "membre"},
        {"id": 4, "email": "elysekongo17@gmail.com", "mot_de_passe": "$2b$12$etOlDiOUTqWZog0ulL48OueawNJ5GYtNUHy7VvhZxzdvOFitap9Fy", "role": "membre"},
        {"id": 5, "email": "gracesylvia792@gmail.com", "mot_de_passe": "$2b$12$shsyB/X3iiI0nBIhAEoO5.fvGYlyilMfDM./RYGA4fitp//LjUV8e", "role": "membre"},
    ]
    for u in users:
        if not Utilisateur.query.filter_by(email=u["email"]).first():
            user = Utilisateur(email=u["email"], role=u["role"])
            user.mot_de_passe = u["mot_de_passe"]
            user.email_verifie = True
            user.tel_verifie = True
            user.kyc_valide = True
            user.compte_actif = True
            db.session.add(user)
    db.session.commit()
    print("Utilisateurs migres avec succes!")
