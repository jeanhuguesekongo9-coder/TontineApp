content = open("app/__init__.py", encoding="utf-8-sig", errors="replace").read()
content = content.replace(
    """    from .scheduler import init_scheduler
    init_scheduler(app)
    return app""",
    """    try:
        from .scheduler import init_scheduler
        init_scheduler(app)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Scheduler non demarre: {e}")
    return app"""
)
open("app/__init__.py", "w", encoding="utf-8").write(content)
print("OK!")
