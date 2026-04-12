from pydantic import BaseModel
from typing import Optional
from datetime import date

class SolicitudInput(BaseModel):
    compania: str
    solicitud_id: str
    solicitud_descripcion: str

class SolicitudOutput(BaseModel):
    compania: str
    solicitud_id: str
    solicitud_fecha: date
    solicitud_tipo: Optional[str] = None
    solicitud_prioridad: Optional[str] = None
    solicitud_id_cliente: Optional[str] = None
    solicitud_tipo_id_cliente: Optional[str] = None
    solicitud_id_plataforma_externa: Optional[str] = None
    proximo_paso: str
    justificacion: str
    estado: str