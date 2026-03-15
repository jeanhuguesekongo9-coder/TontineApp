content = open("app/templates/contrats/contrat.html", encoding="utf-8-sig", errors="replace").read()

ancien_sig = """        <!-- Signatures -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;margin:30px 0;padding:20px;background:#f8f9fa;border-radius:12px;">
          <div style="text-align:center;border-right:1px solid #dee2e6;padding-right:20px;">
            <p style="font-size:0.8rem;color:#999;margin-bottom:10px;">SIGNATURE DU PARTICIPANT</p>
            <div style="border-bottom:2px solid #1a1a2e;height:50px;margin-bottom:8px;display:flex;align-items:flex-end;justify-content:center;">
              <span style="font-size:0.75rem;color:#aaa;padding-bottom:4px;">Signature électronique au moment de la validation</span>
            </div>
            <p style="font-size:0.85rem;font-weight:600;color:#1a1a2e;">{{ membre_nom }}</p>
            <p style="font-size:0.75rem;color:#666;">{{ membre_email }}</p>
          </div>
          <div style="text-align:center;padding-left:20px;">
            <p style="font-size:0.8rem;color:#999;margin-bottom:10px;">SIGNATURE DE TONTINESECURE</p>
            <div style="border-bottom:2px solid #f0a500;height:50px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;">
              <span style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:800;color:#f0a500;font-style:italic;">TontineSecure</span>
            </div>
            <p style="font-size:0.85rem;font-weight:600;color:#1a1a2e;">La Direction Générale</p>
            <p style="font-size:0.75rem;color:#666;">Société de gestion de tontines sécurisées</p>
            <div style="margin-top:8px;padding:6px 12px;background:#1a1a2e;border-radius:20px;display:inline-block;">
              <span style="color:#f0a500;font-size:0.7rem;font-weight:700;">CACHET OFFICIEL</span>
            </div>
          </div>
        </div>"""

nouveau_sig = """        <!-- Signatures -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:30px 0;">
          <!-- Signature TontineSecure a gauche -->
          <div style="text-align:center;padding:20px;background:#f8f9fa;border-radius:12px;">
            <p style="font-size:0.75rem;color:#999;font-weight:600;letter-spacing:1px;margin-bottom:12px;">TONTINESECURE SARL</p>
            <div style="border-bottom:2px solid #1a1a2e;height:45px;margin-bottom:10px;display:flex;align-items:center;justify-content:center;">
              <span style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;color:#1a1a2e;font-style:italic;">TontineSecure</span>
            </div>
            <p style="font-size:0.82rem;color:#444;margin-bottom:4px;">Direction Générale</p>
            <p style="font-size:0.82rem;color:#444;margin-bottom:12px;">TontineSecure SARL</p>
            <div style="background:#27ae60;color:#fff;border-radius:20px;padding:6px 16px;display:inline-flex;align-items:center;gap:6px;">
              <span style="font-size:0.8rem;font-weight:700;">✅ SIGNÉ ÉLECTRONIQUEMENT</span>
            </div>
          </div>
          <!-- Signature membre a droite -->
          <div style="text-align:center;padding:20px;background:#f8f9fa;border-radius:12px;border:2px dashed #dee2e6;">
            <p style="font-size:0.75rem;color:#999;font-weight:600;letter-spacing:1px;margin-bottom:12px;">LE PARTICIPANT</p>
            <div style="border-bottom:2px dashed #dee2e6;height:45px;margin-bottom:10px;display:flex;align-items:center;justify-content:center;">
              <span style="font-size:0.75rem;color:#bbb;font-style:italic;">Signature apposée à la validation</span>
            </div>
            <p style="font-size:0.82rem;color:#444;margin-bottom:4px;">{{ membre_nom }}</p>
            <p style="font-size:0.75rem;color:#666;margin-bottom:12px;">{{ membre_email }}</p>
            <div style="background:#fff3cd;color:#856404;border-radius:20px;padding:6px 16px;display:inline-flex;align-items:center;gap:6px;border:1px solid #ffc107;">
              <span style="font-size:0.8rem;font-weight:700;">⏳ En attente de votre signature</span>
            </div>
          </div>
        </div>"""

content = content.replace(ancien_sig, nouveau_sig)
open("app/templates/contrats/contrat.html", "w", encoding="utf-8").write(content)
print("Signature TontineSecure SIGNE present :", "SIGNÉ ÉLECTRONIQUEMENT" in content)
print("En attente present :", "En attente de votre signature" in content)
print("OK!")
