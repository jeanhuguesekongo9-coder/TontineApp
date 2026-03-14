content = open("app/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    "    return app",
    """    from .scheduler import init_scheduler
    init_scheduler(app)
    return app"""
)
open("app/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
