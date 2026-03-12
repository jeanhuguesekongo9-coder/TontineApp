lines = open("requirements.txt", encoding="utf-8-sig", errors="replace").readlines()
# Garder seulement les lignes propres, enlever les lignes corrompues avec supabase
lines_propres = [l for l in lines if "supabase" not in l.lower() and "\x00" not in l]
# Ajouter supabase proprement
lines_propres.append("supabase==2.28.0\n")
open("requirements.txt", "w", encoding="utf-8").write("".join(lines_propres))
print("requirements.txt corrige !")
print(open("requirements.txt", encoding="utf-8").read())
