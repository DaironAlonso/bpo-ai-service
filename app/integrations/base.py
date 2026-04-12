from abc import ABC, abstractmethod

class ExternalPlatform(ABC):
    @abstractmethod
    def crear_caso(self, solicitud_id: str, descripcion: str, tipo: str, prioridad: str) -> str:
        """Retorna el ID del caso en la plataforma externa."""
        pass