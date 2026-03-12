content = open("config.py", encoding="utf-8-sig", errors="replace").read()
paniers = """
    PANIERS = [
        {"montant": 50000, "label": "50 000 FCFA/mois"},
        {"montant": 100000, "label": "100 000 FCFA/mois"},
        {"montant": 200000, "label": "200 000 FCFA/mois"},
    ]
"""
content = content.replace("class Config:", "class Config:" + paniers)
open("config.py", "w", encoding="utf-8").write(content)
print("OK!")
