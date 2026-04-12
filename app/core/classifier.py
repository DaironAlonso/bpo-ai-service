from app.llm.groq_client import call_llm
import json

SYSTEM_PROMPT = """Eres un clasificador de solicitudes BPO. Dado el texto de una solicitud y las 
categorías disponibles para la empresa, debes:
1. Asignar la categoría más apropiada de la lista.
2. Asignar prioridad: Alta, Media o Baja según urgencia e impacto.
3. Extraer el tipo de documento del cliente (CC, NIT, CE, etc.) si aparece.
4. Extraer el número de documento del cliente si aparece.
5. Redactar una justificación breve de la prioridad asignada.

Responde SOLO con JSON:
{
  "tipo": "...",
  "prioridad": "Alta|Media|Baja",
  "tipo_id_cliente": "CC|NIT|CE|Desconocido",
  "numero_id_cliente": "...",
  "justificacion": "..."
}"""

def clasificar_solicitud(descripcion: str, categorias: list, prioridad_override: str = None) -> dict:
    user_prompt = f"Categorías disponibles: {json.dumps(categorias)}\n\nSolicitud: {descripcion}"
    result = call_llm(SYSTEM_PROMPT, user_prompt)
    if prioridad_override:
        result["prioridad"] = prioridad_override
        result["justificacion"] += f" [Prioridad determinada por servicio externo del cliente]"
    return result