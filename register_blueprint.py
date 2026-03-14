content = open("app/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    "    from .main import main as main_bp\n    app.register_blueprint(main_bp)",
    "    from .main import main as main_bp\n    app.register_blueprint(main_bp)\n    from .paiements import paiements as paiements_bp\n    app.register_blueprint(paiements_bp, url_prefix=\"/paiements\")"
)
open("app/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
