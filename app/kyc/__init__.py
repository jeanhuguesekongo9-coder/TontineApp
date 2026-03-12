from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os, secrets
from ..models import db, KYC, AuditLog

kyc = Blueprint("kyc", __name__)

def sauvegarder_fichier(fichier, sous_dossier):
    if not fichier or fichier.filename == "":
        return None
    ext = fichier.filename.rsplit(".", 1)[-1].lower()
    if ext not in {"pdf", "jpg", "jpeg", "png"}:
        return None
    import os, secrets
    from supabase import create_client
    nom = secrets.token_hex(16) + "." + ext
    chemin = sous_dossier + "/" + nom
    try:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        client = create_client(url, key)
        data = fichier.read()
        client.storage.from_("kyc-documents").upload(chemin, data, {"content-type": fichier.mimetype})
        return chemin
    except Exception as e:
        print(f"Erreur Supabase upload: {e}")
        return None

@kyc.route("/soumettre", methods=["GET", "POST"])
@login_required
def soumettre():
    if not current_user.tel_verifie:
        flash("Verifiez d abord votre telephone.", "warning")
        return redirect(url_for("auth.verifier_telephone"))
    kyc_existant = current_user.kyc
    if kyc_existant and kyc_existant.statut == "approuve":
        return redirect(url_for("main.tableau_de_bord"))
    if request.method == "POST":
        type_doc = request.form.get("type_doc")
        rib = request.form.get("rib", "").strip().upper().replace(" ", "")
        banque = request.form.get("banque", "").strip()
        doc_identite = request.files.get("doc_identite")
        doc_identite2 = request.files.get("doc_identite2")
        bulletin = request.files.get("bulletin_salaire")
        photo = request.files.get("photo_profil")
        if not doc_identite or not bulletin:
            flash("Document identite et bulletin sont obligatoires.", "danger")
            return render_template("kyc/soumettre.html", kyc=kyc_existant)
        chemin1 = sauvegarder_fichier(doc_identite, "identites")
        chemin2 = sauvegarder_fichier(doc_identite2, "identites") if doc_identite2 else None
        chemin_b = sauvegarder_fichier(bulletin, "bulletins")
        chemin_p = sauvegarder_fichier(photo, "photos") if photo else None
        if not chemin1 or not chemin_b:
            flash("Erreur upload. Verifiez le format (PDF/JPG/PNG).", "danger")
            return render_template("kyc/soumettre.html", kyc=kyc_existant)
        if rib:
            current_user.profil.rib = rib
        if banque:
            current_user.profil.banque = banque
        if chemin_p:
            current_user.profil.photo_profil = chemin_p
        if kyc_existant:
            kyc_existant.type_doc = type_doc
            kyc_existant.doc_identite = chemin1
            kyc_existant.doc_identite2 = chemin2
            kyc_existant.bulletin_salaire = chemin_b
            kyc_existant.statut = "en_attente"
            kyc_existant.note_admin = None
        else:
            nouveau = KYC(user_id=current_user.id, type_doc=type_doc,
                doc_identite=chemin1, doc_identite2=chemin2,
                bulletin_salaire=chemin_b, statut="en_attente")
            db.session.add(nouveau)
        db.session.commit()
        AuditLog.log(current_user.id, "kyc_soumis", ip=request.remote_addr)
        db.session.commit()
        flash("Dossier soumis ! Verification sous 24-48h.", "success")
        return redirect(url_for("kyc.statut"))
    return render_template("kyc/soumettre.html", kyc=kyc_existant)

@kyc.route("/statut")
@login_required
def statut():
    return render_template("kyc/statut.html", kyc=current_user.kyc)
