from fastapi import APIRouter, HTTPException
from app.models.schemas import SolicitudInput, SolicitudOutput
from app.core.pipeline import procesar_solicitud

router = APIRouter()

@router.post("/procesar", response_model=SolicitudOutput)
def procesar(solicitud: SolicitudInput):
    try:
        return procesar_solicitud(solicitud)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")