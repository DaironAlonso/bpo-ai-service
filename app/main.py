from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="BPO AI Microservice",
    description="Automatización de gestión de solicitudes BPO con IA",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}