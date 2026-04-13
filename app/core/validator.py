from app.llm.groq_client import call_llm

SYSTEM_PROMPT = """Eres un validador de solicitudes BPO. Tu tarea es determinar si una solicitud 
tiene la información mínima necesaria para ser gestionada.

Una solicitud ES VÁLIDA si:
- Describe un incidente con qué pasó, cuándo y qué necesita, O
- Es una consulta informativa simple (horarios, canales, precios, procedimientos), O
- El usuario se identifica y expresa claramente qué necesita.

Una solicitud NO ES VÁLIDA solo si es completamente vaga sin ningún contexto 
(ej: "tengo un problema", "necesito ayuda", "quiero información").

Responde SOLO con JSON: {"valida": true/false, "razon": "..."}"""

def validar_solicitud(descripcion: str) -> dict:
    return call_llm(SYSTEM_PROMPT, f"Solicitud: {descripcion}")