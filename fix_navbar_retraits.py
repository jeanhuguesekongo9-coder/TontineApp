content = open("app/templates/base.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    """<li class="nav-item"><a class="nav-link" href="{{ url_for('paiements.mes_retraits') }}">💸 Mes Retraits</a></li>""",
    ""
)
open("app/templates/base.html", "w", encoding="utf-8").write(content)
print("OK!")
