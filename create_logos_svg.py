import os
os.makedirs("app/static/logos", exist_ok=True)

# Logo Wave - SVG pur
wave_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" rx="30" fill="#1DC8EE"/>
<path d="M20 130 Q50 50 80 100 Q110 150 140 70 Q160 30 180 80" stroke="white" stroke-width="18" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# Logo Orange Money - SVG pur
orange_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" rx="100" fill="#FF6600"/>
<text x="100" y="125" font-family="Arial Black" font-size="90" font-weight="900" fill="white" text-anchor="middle">O</text>
</svg>"""

# Logo MTN - SVG pur
mtn_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" rx="20" fill="#FFCC00"/>
<text x="100" y="120" font-family="Arial Black" font-size="52" font-weight="900" fill="#1a1a2e" text-anchor="middle">MTN</text>
<text x="100" y="160" font-family="Arial" font-size="24" fill="#1a1a2e" text-anchor="middle">MoMo</text>
</svg>"""

open("app/static/logos/wave.svg", "w", encoding="utf-8").write(wave_svg)
open("app/static/logos/orange.svg", "w", encoding="utf-8").write(orange_svg)
open("app/static/logos/mtn.svg", "w", encoding="utf-8").write(mtn_svg)
print("OK! 3 logos SVG crees")
