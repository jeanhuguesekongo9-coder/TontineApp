import re
content = open("app/templates/paiements/recharger.html", encoding="utf-8-sig", errors="replace").read()

# Wave SN
content = re.sub(
    r'<div style="width:52px.*?</div>\s*<div style="font-weight:700.*?>Wave Senegal</div>',
    '<img src="/static/logos/wave.svg" style="width:52px;height:52px;border-radius:12px;margin:0 auto 6px;display:block;"><div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Senegal</div>',
    content, flags=re.DOTALL, count=1
)
# Wave CI
content = re.sub(
    r'<div style="width:52px.*?</div>\s*<div style="font-weight:700.*?>Wave Cote d Ivoire</div>',
    '<img src="/static/logos/wave.svg" style="width:52px;height:52px;border-radius:12px;margin:0 auto 6px;display:block;"><div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Wave Cote d Ivoire</div>',
    content, flags=re.DOTALL, count=1
)
# Orange SN
content = re.sub(
    r'<div style="width:52px.*?</div>\s*<div style="font-weight:700.*?>Orange Money SN</div>',
    '<img src="/static/logos/orange.svg" style="width:52px;height:52px;border-radius:50%;margin:0 auto 6px;display:block;"><div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money SN</div>',
    content, flags=re.DOTALL, count=1
)
# Orange CI
content = re.sub(
    r'<div style="width:52px.*?</div>\s*<div style="font-weight:700.*?>Orange Money CI</div>',
    '<img src="/static/logos/orange.svg" style="width:52px;height:52px;border-radius:50%;margin:0 auto 6px;display:block;"><div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">Orange Money CI</div>',
    content, flags=re.DOTALL, count=1
)
# MTN CI
content = re.sub(
    r'<div style="width:52px.*?</div>\s*<div style="font-weight:700.*?>MTN MoMo CI</div>',
    '<img src="/static/logos/mtn.svg" style="width:52px;height:52px;border-radius:12px;margin:0 auto 6px;display:block;"><div style="font-weight:700;font-size:0.82rem;color:#1a1a2e;">MTN MoMo CI</div>',
    content, flags=re.DOTALL, count=1
)
open("app/templates/paiements/recharger.html", "w", encoding="utf-8").write(content)
print("OK!")
