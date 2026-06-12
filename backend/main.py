from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

STATIC_DIR = "/app/static"


@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI"}


@app.get("/", response_class=HTMLResponse)
async def index():
    return """<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Kanban Studio</title></head>
<body>
<h1>Hello World</h1>
<p>Le serveur FastAPI fonctionne.</p>
</body>
</html>"""
