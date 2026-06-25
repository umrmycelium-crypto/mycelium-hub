from fastapi.staticfiles import StaticFiles

def mount_static(app):
    app.mount("/", StaticFiles(directory="mycelium/runtime/static", html=True), name="static")
