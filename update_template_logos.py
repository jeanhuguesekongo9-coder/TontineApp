content = open("app/templates/paiements/recharger.html", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    '                <div style="font-size:1.8rem;">{{ info.flag }}</div>',
    '                {% if info.logo %}<img src="{{ info.logo }}" style="height:40px;object-fit:contain;margin-bottom:5px;" onerror="this.style.display=\'none\'">{% else %}<div style="font-size:1.8rem;">{{ info.flag }}</div>{% endif %}'
)
open("app/templates/paiements/recharger.html", "w", encoding="utf-8").write(content)
print("OK!")
