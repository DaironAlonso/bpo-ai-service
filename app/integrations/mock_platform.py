import uuid
from app.integrations.base import ExternalPlatform

class MockPlatform(ExternalPlatform):
    # Registro en memoria para evitar duplicados
    _casos_registrados: dict = {}

    def crear_caso(self, solicitud_id: str, descripcion: str, tipo: str, prioridad: str) -> str:
        if solicitud_id in self._casos_registrados:
            # Retorna el mismo ID si ya fue creado (idempotencia, evita duplicados)
            return self._casos_registrados[solicitud_id]
        caso_id = f"ID{uuid.uuid4().hex[:9].upper()}"
        self._casos_registrados[solicitud_id] = caso_id
        return caso_id

def get_platform(plataforma: str) -> ExternalPlatform:
    # Factory: en el futuro se mapean más plataformas aquí
    return MockPlatform()