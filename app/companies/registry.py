# Registro central de empresas. Para agregar una nueva, solo se añade aquí.
COMPANIES = {
    "GASES DEL ORINOCO": {
        "categorias": ["Incidente técnico", "Solicitud de información", "Queja", "Solicitud administrativa"],
        "delegaciones_externas": ["Incidente técnico", "Queja"],
        "plataforma": "mock",
    },
    "MENSAJERIA DEL VALLE": {
        "categorias": ["Paquete perdido", "Retraso en entrega", "Solicitud de información", "Cambio de dirección"],
        "delegaciones_externas": ["Paquete perdido", "Retraso en entrega"],
        "plataforma": "mock",
        "prioridad_externa": True,  # Este cliente provee su propio servicio de prioridad
    },
    "BANCO CENTRAL": {
        "categorias": ["Fraude", "Consulta de saldo", "Bloqueo de tarjeta", "Solicitud de crédito"],
        "delegaciones_externas": ["Fraude", "Bloqueo de tarjeta", "Solicitud de crédito"],
        "plataforma": "mock",
    },
    "SALUD TOTAL": {
        "categorias": ["Autorización médica", "Queja", "Solicitud de información", "Reembolso"],
        "delegaciones_externas": ["Autorización médica", "Reembolso"],
        "plataforma": "mock",
    },
}

def get_company_config(compania: str) -> dict:
    config = COMPANIES.get(compania.upper())
    if not config:
        raise ValueError(f"Empresa '{compania}' no está parametrizada en el sistema.")
    return config