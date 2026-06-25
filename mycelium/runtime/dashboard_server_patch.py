from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="mycelium/runtime/static", html=True), name="static")

@app.get("/health")
def health():
    return {"status": "mycelium-live-graph"}
