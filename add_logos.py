content = open("app/paiements/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    '"wave_sn": {"nom": "Wave Senegal", "numero": "+221 77 XXX XX XX", "flag": "🇸🇳"}',
    '"wave_sn": {"nom": "Wave Senegal", "numero": "+221 77 XXX XX XX", "flag": "🇸🇳", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Wave_money_logo.svg/200px-Wave_money_logo.svg.png"}'
)
content = content.replace(
    '"wave_ci": {"nom": "Wave Cote d Ivoire", "numero": "+225 07 XXX XX XX", "flag": "🇨🇮"}',
    '"wave_ci": {"nom": "Wave Cote d Ivoire", "numero": "+225 07 XXX XX XX", "flag": "🇨🇮", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Wave_money_logo.svg/200px-Wave_money_logo.svg.png"}'
)
content = content.replace(
    '"orange_sn": {"nom": "Orange Money Senegal", "numero": "+221 77 XXX XX XX", "flag": "🇸🇳"}',
    '"orange_sn": {"nom": "Orange Money Senegal", "numero": "+221 77 XXX XX XX", "flag": "🇸🇳", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Orange_logo.svg/200px-Orange_logo.svg.png"}'
)
content = content.replace(
    '"orange_ci": {"nom": "Orange Money CI", "numero": "+225 07 XXX XX XX", "flag": "🇨🇮"}',
    '"orange_ci": {"nom": "Orange Money CI", "numero": "+225 07 XXX XX XX", "flag": "🇨🇮", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Orange_logo.svg/200px-Orange_logo.svg.png"}'
)
content = content.replace(
    '"mtn_ci": {"nom": "MTN CI", "numero": "+225 05 XXX XX XX", "flag": "🇨🇮"}',
    '"mtn_ci": {"nom": "MTN CI", "numero": "+225 05 XXX XX XX", "flag": "🇨🇮", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/MTN_Logo.svg/200px-MTN_Logo.svg.png"}'
)
open("app/paiements/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
