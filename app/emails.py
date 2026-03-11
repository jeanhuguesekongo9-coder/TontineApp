# -*- coding: utf-8 -*-
from flask_mail import Message
from flask import url_for, current_app
from app import mail

def envoyer_email_verification(utilisateur):
    token = utilisateur.generer_token_email()
    from app.models import db
    db.session.commit()
    lien = url_for('auth.verifier_email', token=token, _external=True)
    msg = Message(
        subject="Verifiez votre email - TontineSecure",
        recipients=[utilisateur.email],
        html=f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
            <div style="background:#1a1a2e;padding:30px;text-align:center;">
                <h1 style="color:#f0a500;margin:0;">TontineSecure</h1>
                <p style="color:#fff;margin:5px 0;">Epargne collaborative securisee</p>
            </div>
            <div style="background:#fff;padding:40px;border:1px solid #eee;">
                <h2 style="color:#1a1a2e;">Bienvenue !</h2>
                <p style="color:#555;">Merci de vous etre inscrit sur TontineSecure.</p>
                <p style="color:#555;">Cliquez sur le bouton ci-dessous pour verifier votre adresse email :</p>
                <div style="text-align:center;margin:30px 0;">
                    <a href="{lien}" style="background:#f0a500;color:#fff;padding:15px 30px;border-radius:10px;text-decoration:none;font-weight:bold;font-size:16px;">
                        Verifier mon email
                    </a>
                </div>
                <p style="color:#999;font-size:13px;">Ce lien expire dans 24 heures.</p>
                <p style="color:#999;font-size:13px;">Si vous n avez pas cree de compte, ignorez cet email.</p>
            </div>
            <div style="background:#f8f8f8;padding:20px;text-align:center;">
                <p style="color:#999;font-size:12px;">TontineSecure — Cote d Ivoire & Senegal</p>
            </div>
        </div>
        """
    )
    mail.send(msg)

def envoyer_email_bienvenue(utilisateur):
    msg = Message(
        subject="Bienvenue sur TontineSecure !",
        recipients=[utilisateur.email],
        html=f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
            <div style="background:#1a1a2e;padding:30px;text-align:center;">
                <h1 style="color:#f0a500;margin:0;">TontineSecure</h1>
            </div>
            <div style="background:#fff;padding:40px;">
                <h2 style="color:#1a1a2e;">Votre compte est verifie !</h2>
                <p style="color:#555;">Votre email a ete verifie avec succes.</p>
                <p style="color:#555;">Completez maintenant votre profil pour rejoindre une tontine.</p>
                <div style="background:#f0f8ff;padding:20px;border-radius:10px;margin:20px 0;">
                    <h3 style="color:#1a1a2e;">Prochaines etapes :</h3>
                    <p style="color:#555;">1. Completer votre profil</p>
                    <p style="color:#555;">2. Soumettre vos documents KYC</p>
                    <p style="color:#555;">3. Rejoindre une tontine</p>
                </div>
            </div>
        </div>
        """
    )
    mail.send(msg)
