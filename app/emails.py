# -*- coding: utf-8 -*-
import socket
from flask_mail import Message
from flask import url_for
from app import mail

def envoyer_email_verification(utilisateur):
    token = utilisateur.generer_token_email()
    from app.models import db
    db.session.commit()
    lien = url_for('auth.verifier_email', token=token, _external=True)
    msg = Message(
        subject="Verifiez votre email - TontineSecure",
        recipients=[utilisateur.email],
        html=f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
            <div style="background:#1a1a2e;padding:30px;text-align:center;">
                <h1 style="color:#f0a500;margin:0;">TontineSecure</h1>
                <p style="color:#fff;margin:5px 0;">Epargne collaborative securisee</p>
            </div>
            <div style="background:#fff;padding:40px;border:1px solid #eee;">
                <h2 style="color:#1a1a2e;">Bienvenue !</h2>
                <p style="color:#555;">Cliquez sur le bouton ci-dessous pour verifier votre email :</p>
                <div style="text-align:center;margin:30px 0;">
                    <a href="{lien}" style="background:#f0a500;color:#fff;padding:15px 30px;border-radius:10px;text-decoration:none;font-weight:bold;font-size:16px;">
                        Verifier mon email
                    </a>
                </div>
                <p style="color:#999;font-size:13px;">Ce lien expire dans 24 heures.</p>
            </div>
        </div>"""
    )
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(10)
    try:
        mail.send(msg)
    finally:
        socket.setdefaulttimeout(old_timeout)

def envoyer_email_bienvenue(utilisateur):
    pass
