# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import config
from .models import db, bcrypt, Utilisateur

migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()

login_manager.login_view = "auth.connexion"
login_manager.login_message = "Veuillez vous connecter pour acceder a cette page."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from .kyc import kyc as kyc_bp
    app.register_blueprint(kyc_bp, url_prefix="/kyc")
    from .tontines import tontines as tontines_bp
    app.register_blueprint(tontines_bp, url_prefix="/tontines")
    from .contrats import contrats as contrats_bp
    app.register_blueprint(contrats_bp, url_prefix="/contrats")
    from .admin import admin as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    from .paiements import paiements as paiements_bp
    app.register_blueprint(paiements_bp, url_prefix="/paiements")

    @app.context_processor
    def inject_globals():
        from flask_login import current_user
        notifs = []
        if current_user.is_authenticated:
            from .models import Notification
            notifs = Notification.query.filter_by(
                user_id=current_user.id, lue=False
            ).order_by(Notification.created_at.desc()).limit(5).all()
        return dict(notifications_non_lues=notifs)

    return app
