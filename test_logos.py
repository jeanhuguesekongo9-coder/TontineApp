content = open("app/templates/paiements/recharger.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    "RESEAUX = {",
    "RESEAUX_LOGOS = {"
)
open("app/paiements/__init__.py", encoding="utf-8-sig", errors="replace").read()

logos = {
    "wave_sn": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Wave_money_logo.svg/1200px-Wave_money_logo.svg.png",
    "wave_ci": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Wave_money_logo.svg/1200px-Wave_money_logo.svg.png",
    "orange_sn": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Orange_logo.svg/1200px-Orange_logo.svg.png",
    "orange_ci": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Orange_logo.svg/1200px-Orange_logo.svg.png",
    "mtn_ci": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/MTN_Logo.svg/1200px-MTN_Logo.svg.png"
}
print(logos)
