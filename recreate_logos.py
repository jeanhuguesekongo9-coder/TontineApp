import os
os.makedirs("app/static/logos", exist_ok=True)

# Logo Wave - Pingouin simplifie
wave_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" rx="40" fill="#1DC8EE"/>
<ellipse cx="100" cy="110" rx="45" ry="55" fill="#1a1a2e"/>
<ellipse cx="100" cy="85" rx="28" ry="32" fill="#f0f0f0"/>
<ellipse cx="88" cy="78" rx="8" ry="9" fill="#1a1a2e"/>
<ellipse cx="112" cy="78" rx="8" ry="9" fill="#1a1a2e"/>
<ellipse cx="88" cy="76" rx="3" ry="3" fill="white"/>
<ellipse cx="112" cy="76" rx="3" ry="3" fill="white"/>
<ellipse cx="100" cy="95" rx="10" ry="7" fill="#f0a500"/>
<ellipse cx="75" cy="130" rx="18" ry="10" fill="#f0a500"/>
<ellipse cx="125" cy="130" rx="18" ry="10" fill="#f0a500"/>
<path d="M65 105 Q55 120 60 140 Q65 155 75 150" fill="#1a1a2e"/>
<path d="M135 105 Q145 120 140 140 Q135 155 125 150" fill="#1a1a2e"/>
</svg>"""

# Logo Orange Money - Fleches orange
orange_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" fill="white"/>
<rect width="200" height="200" fill="#FF6600" opacity="0.08"/>
<g transform="translate(20,20)">
  <polygon points="45,0 160,0 160,30 75,30 75,115 45,115" fill="#FF6600"/>
  <polygon points="115,160 0,160 0,130 85,130 85,45 115,45" fill="#1a1a2e"/>
  <polygon points="130,145 160,115 160,160 115,160" fill="#FF6600"/>
  <polygon points="30,15 0,45 0,0 45,0" fill="#1a1a2e"/>
</g>
</svg>"""

# Logo MTN MoMo - Bleu marine avec cornes jaunes
mtn_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" rx="35" fill="#003580"/>
<path d="M30 60 Q60 20 100 50 Q140 20 170 60 L170 80 Q140 45 100 70 Q60 45 30 80 Z" fill="#FFCC00"/>
<circle cx="100" cy="125" r="35" fill="#FFCC00"/>
<text x="100" y="133" font-family="Arial Black" font-size="22" font-weight="900" fill="#003580" text-anchor="middle">MoMo</text>
</svg>"""

open("app/static/logos/wave.svg", "w", encoding="utf-8").write(wave_svg)
open("app/static/logos/orange.svg", "w", encoding="utf-8").write(orange_svg)
open("app/static/logos/mtn.svg", "w", encoding="utf-8").write(mtn_svg)
print("OK! 3 logos SVG recrees")
