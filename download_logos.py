import os, urllib.request

os.makedirs("app/static/logos", exist_ok=True)

logos = {
    "wave.png": "https://cdn.worldvectorlogo.com/logos/wave-3.svg",
    "orange.png": "https://cdn.worldvectorlogo.com/logos/orange-1.svg",
    "mtn.png": "https://cdn.worldvectorlogo.com/logos/mtn-1.svg"
}

headers = {"User-Agent": "Mozilla/5.0"}
for nom, url in logos.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            open(f"app/static/logos/{nom}", "wb").write(r.read())
            print(f"OK {nom}!")
    except Exception as e:
        print(f"ERREUR {nom}: {e}")
