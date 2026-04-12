# BPO AI Microservice

Microservicio de IA para automatización de gestión de solicitudes BPO.

## Requisitos
- Python 3.10+
- Cuenta en [Groq](https://console.groq.com/keys) (gratis)

## Configuración

```bash
git clone <repo-url>
cd bpo-ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env
# Editar .env y poner tu GROQ_API_KEY
```

## Ejecución local

```bash
uvicorn app.main:app --reload
```

Documentación interactiva: http://localhost:8000/docs

---

## Ejemplos de uso

### Caso 1 — Gestión externa (incidente técnico)

```bash
curl -X POST http://localhost:8000/api/v1/procesar \
  -H "Content-Type: application/json" \
  -d '{
    "compania": "GASES DEL ORINOCO",
    "solicitud_id": "REQ-001",
    "solicitud_descripcion": "Mi nombre es Juana y mi numero de cedula es 102045678. Solicito una revision urgente porque la estufa que compre hace 2 semanas presenta fallas, no esta haciendo contacto con la llave del gas."
  }'
```

**Respuesta esperada:**
```json
{
  "compania": "GASES DEL ORINOCO",
  "solicitud_id": "REQ-001",
  "solicitud_fecha": "2026-04-12",
  "solicitud_tipo": "Incidente técnico",
  "solicitud_prioridad": "Alta",
  "solicitud_id_cliente": "CC",
  "solicitud_tipo_id_cliente": "102045678",
  "solicitud_id_plataforma_externa": "ID8CAD0417C",
  "proximo_paso": "GESTION_EXTERNA",
  "justificacion": "Falla técnica en estufa de gas que requiere intervención presencial urgente.",
  "estado": "pendiente"
}
```

---

### Caso 2 — Información incompleta

```bash
curl -X POST http://localhost:8000/api/v1/procesar \
  -H "Content-Type: application/json" \
  -d '{
    "compania": "GASES DEL ORINOCO",
    "solicitud_id": "REQ-002",
    "solicitud_descripcion": "Tengo un problema"
  }'
```

**Respuesta esperada:**
```json
{
  "compania": "GASES DEL ORINOCO",
  "solicitud_id": "REQ-002",
  "solicitud_fecha": "2026-04-12",
  "solicitud_tipo": null,
  "solicitud_prioridad": null,
  "proximo_paso": "CIERRE_POR_INFORMACION_INSUFICIENTE",
  "justificacion": "La solicitud no contiene información mínima: no se especifica qué ocurrió, cuándo ni qué necesita el usuario.",
  "estado": "cerrado"
}
```

---

### Caso 3 — Empresa no parametrizada (error controlado)

```bash
curl -X POST http://localhost:8000/api/v1/procesar \
  -H "Content-Type: application/json" \
  -d '{
    "compania": "EMPRESA FANTASMA",
    "solicitud_id": "REQ-003",
    "solicitud_descripcion": "Necesito ayuda urgente con mi servicio desde hace una semana."
  }'
```

**Respuesta esperada:**
```json
{
  "detail": "Empresa 'EMPRESA FANTASMA' no está parametrizada en el sistema."
}
```
> HTTP 422 — La empresa no existe en el registry.

---

### Caso 4 — MENSAJERIA DEL VALLE (prioridad externa)

```bash
curl -X POST http://localhost:8000/api/v1/procesar \
  -H "Content-Type: application/json" \
  -d '{
    "compania": "MENSAJERIA DEL VALLE",
    "solicitud_id": "REQ-004",
    "solicitud_descripcion": "Soy Carlos Gomez con cedula 55678901. Mi paquete enviado hace 5 dias no ha llegado y es urgente porque contiene medicamentos."
  }'
```

**Respuesta esperada:**
```json
{
  "compania": "MENSAJERIA DEL VALLE",
  "solicitud_id": "REQ-004",
  "solicitud_fecha": "2026-04-12",
  "solicitud_tipo": "Paquete perdido",
  "solicitud_prioridad": "Alta",
  "solicitud_id_cliente": "CC",
  "solicitud_tipo_id_cliente": "55678901",
  "solicitud_id_plataforma_externa": "ID2FA9C3E1B",
  "proximo_paso": "GESTION_EXTERNA",
  "justificacion": "Prioridad Alta asignada por servicio externo del cliente. Paquete no entregado con contenido de carácter urgente.",
  "estado": "pendiente"
}
```
> La prioridad fue determinada por el microservicio externo de MENSAJERIA DEL VALLE, no por el LLM.

---

### Caso 5 — Respuesta directa (consulta informativa)

```bash
curl -X POST http://localhost:8000/api/v1/procesar \
  -H "Content-Type: application/json" \
  -d '{
    "compania": "GASES DEL ORINOCO",
    "solicitud_id": "REQ-005",
    "solicitud_descripcion": "Buenos dias, quisiera saber cual es el horario de atencion al cliente de la empresa y los canales de contacto disponibles."
  }'
```

**Respuesta esperada:**
```json
{
  "compania": "GASES DEL ORINOCO",
  "solicitud_id": "REQ-005",
  "solicitud_fecha": "2026-04-12",
  "solicitud_tipo": "Solicitud de información",
  "solicitud_prioridad": "Baja",
  "solicitud_id_plataforma_externa": null,
  "proximo_paso": "RESPUESTA_DIRECTA",
  "justificacion": "Consulta informativa que puede ser resuelta directamente por el BPO sin gestión externa.",
  "estado": "cerrado"
}
```

---

## Agregar una nueva empresa

Solo edita `app/companies/registry.py` y añade la empresa al diccionario `COMPANIES`:

```python
"NUEVA EMPRESA": {
    "categorias": ["Categoría 1", "Categoría 2", "Queja"],
    "delegaciones_externas": ["Categoría 1"],
    "plataforma": "mock",
},
```

## Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `GROQ_API_KEY` | API Key de Groq ([obtener aquí](https://console.groq.com/keys)) |