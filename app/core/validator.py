from app.llm.groq_client import call_llm

SYSTEM_PROMPT = """Eres un validador de solicitudes BPO. Tu tarea es determinar si una solicitud 
tiene la información mínima necesaria para ser gestionada: qué pasó, cuándo o contexto temporal, 
y qué necesita el usuario. Responde SOLO con JSON: {"valida": true/false, "razon": "..."}"""

def validar_solicitud(descripcion: str) -> dict:
    return call_llm(SYSTEM_PROMPT, f"Solicitud: {descripcion}")