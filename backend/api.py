"""
API REST del Clasificador de Spam usando FastAPI

Inicializa la aplicación FastAPI y expone endpoints,
configura middleware CORS, conecta servicios de clasificación ML y
sirve el frontend estático en producción.

Documentación interactiva disponible en /docs (Swagger UI) y /redoc (ReDoc).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from config import BASE_DIR, modelos
from schemas import MensajeRequest, ClasificacionResponse
from clasificador import clasificar

tags_metadata = [
    {
        "name": "Modelos",
        "description": "Listado de modelos ML disponibles para clasificación",
    },
    {
        "name": "Clasificación",
        "description": "Clasificación de mensajes como spam o ham",
    },
    {
        "name": "Frontend",
        "description": "Servir la aplicación web (solo en producción)",
    },
]

app = FastAPI(
    title="Clasificador de Spam",
    description="API REST para clasificar mensajes de texto como **spam** o **ham** usando modelos de Machine Learning entrenados en español.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def redirigir_a_docs():
    return RedirectResponse(url="/docs")

@app.get(
    "/api/modelos",
    tags=["Modelos"],
    summary="Listar modelos disponibles",
    response_description="Lista de nombres de modelos",
)
def listar_modelos():
    # Devuelve los nombres de los modelos ML cargados y listos para usar
    return list(modelos.keys())

@app.post(
    "/api/clasificar",
    tags=["Clasificación"],
    summary="Clasificar un mensaje",
    response_model=ClasificacionResponse,
)
def clasificar_endpoint(req: MensajeRequest):
    # Clasifica un mensaje de texto como spam o ham
    return clasificar(req.mensaje, req.modelo)

@app.get("/{path:path}", tags=["Frontend"], include_in_schema=False)
def servir_frontend(path: str):
    """
    Sirve el frontend estático (SPA).

    En producción usa `frontend/dist/`; en desarrollo redirige
    a /docs para evitar mostrar el HTML fuente sin build.
    """
    dist = os.path.join(BASE_DIR, "frontend", "dist")
    index = os.path.join(dist, "index.html")

    if path == "" or path == "index.html" or not os.path.isfile(os.path.join(dist, path)):
        if os.path.isfile(index):
            return FileResponse(index)
        return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))

    return FileResponse(os.path.join(dist, path))

# Servidor local (reload activo)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )