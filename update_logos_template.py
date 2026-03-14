content = open("app/templates/paiements/recharger.html", encoding="utf-8-sig", errors="replace").read()

# Remplacer les icones SVG inline par les vrais logos locaux
content = content.replace(
    '<div style="width:52px;height:52px;margin:0 auto 6px;border-radius:12px;background:#1DC8EE;display:flex;align-items:center;justify-content:center;">\n                  <svg width="32" height="20" viewBox="0 0 120 60" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 50 Q30 10 50 30 Q70 50 90 10 Q100 5 110 20" stroke="white" stroke-width="10" fill="none" stroke-linecap="round"/></svg>\n                </div>\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Senegal</div>',
    '<img src="/static/logos/wave.svg" style="width:52px;height:52px;border-radius:12px;margin:0 auto 6px;display:block;">\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Senegal</div>'
)
content = content.replace(
    '<div style="width:52px;height:52px;margin:0 auto 6px;border-radius:12px;background:#1DC8EE;display:flex;align-items:center;justify-content:center;">\n                  <svg width="32" height="20" viewBox="0 0 120 60" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 50 Q30 10 50 30 Q70 50 90 10 Q100 5 110 20" stroke="white" stroke-width="10" fill="none" stroke-linecap="round"/></svg>\n                </div>\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Cote d Ivoire</div>',
    '<img src="/static/logos/wave.svg" style="width:52px;height:52px;border-radius:12px;margin:0 auto 6px;display:block;">\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Cote d Ivoire</div>'
)
content = content.replace(
    '<div style="width:52px;height:52px;margin:0 auto 6px;border-radius:50%;background:#FF6600;display:flex;align-items:center;justify-content:center;">\n                  <span style="color:#fff;font-weight:900;font-size:1.3rem;">O</span>\n                </div>\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money SN</div>',
    '<img src="/static/logos/orange.svg" style="width:52px;height:52px;border-radius:50%;margin:0 auto 6px;display:block;">\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money SN</div>'
)
content = content.replace(
    '<div style="width:52px;height:52px;margin:0 auto 6px;border-radius:50%;background:#FF6600;display:flex;align-items:center;justify-content:center;">\n                  <span style="color:#fff;font-weight:900;font-size:1.3rem;">O</span>\n                </div>\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money CI</div>',
    '<img src="/static/logos/orange.svg" style="width:52px;height:52px;border-radius:50%;margin:0 auto 6px;display:block;">\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money CI</div>'
)
content = content.replace(
    '<div style="width:52px;height:52px;margin:0 auto 6px;border-radius:12px;background:#FFCC00;display:flex;align-items:center;justify-content:center;">\n                  <span style="color:#1a1a2e;font-weight:900;font-size:0.8rem;">MTN</span>\n                </div>\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">MTN MoMo CI</div>',
    '<img src="/static/logos/mtn.svg" style="width:52px;height:52px;border-radius:12px;margin:0 auto 6px;display:block;">\n                <div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">MTN MoMo CI</div>'
)
open("app/templates/paiements/recharger.html", "w", encoding="utf-8").write(content)
print("OK!")
