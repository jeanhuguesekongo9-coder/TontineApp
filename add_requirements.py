content = open("requirements.txt", encoding="utf-8-sig", errors="replace").read()
if "apscheduler" not in content:
    content = content.rstrip() + "\napscheduler==3.11.2\n"
    open("requirements.txt", "w", encoding="utf-8").write(content)
    print("OK! apscheduler ajoute")
else:
    print("Deja present!")
