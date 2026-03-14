# Mise a jour navbar + route ma_tontine + liens admin
import re

# 1. Ajouter route ma_tontine dans paiements
content = open("app/paiements/__init__.py", encoding="utf-8-sig", errors="replace").read()
nouvelle_route = """
@paiements.route("/ma-tontine")
@login_required
def ma_tontine():
    from ..models import MembreTontine, Penalite
    memberships = MembreTontine.query.filter_by(user_id=current_user.id).all()
    penalites_actives = Penalite.query.filter(
        Penalite.user_id == current_user.id,
        Penalite.statut.in_(["en_cours", "mise_en_demeure"])
    ).all()
    return render_template("paiements/ma_tontine.html",
        memberships=memberships,
        penalites_actives=penalites_actives)
"""
content = content.rstrip() + nouvelle_route
open("app/paiements/__init__.py", "w", encoding="utf-8").write(content)
print("OK route ma_tontine!")

# 2. Mettre a jour navbar base.html
content = open("app/templates/base.html", encoding="utf-8-sig", errors="replace").read()

# Lien membre Ma Tontine
if "ma-tontine" not in content:
    content = content.replace(
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('paiements.dashboard') }}">💰 Mon Portefeuille</a></li>""",
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('paiements.dashboard') }}">💰 Mon Portefeuille</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('paiements.ma_tontine') }}">🔒 Ma Tontine</a></li>"""
    )

# Lien admin Penalites + Tableau de bord
if "gerer_penalites" not in content:
    content = content.replace(
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.gerer_soldes') }}">💰 Soldes</a></li>""",
        """        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.gerer_soldes') }}">💰 Soldes</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.gerer_penalites') }}">⚠️ Penalites</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.tableau_de_bord') }}">📊 Tableau de bord</a></li>"""
    )

open("app/templates/base.html", "w", encoding="utf-8").write(content)
print("OK navbar mise a jour!")
