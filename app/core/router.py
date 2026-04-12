def determinar_siguiente_paso(tipo: str, config: dict) -> str:
    delegaciones = config.get("delegaciones_externas", [])
    if tipo in delegaciones:
        return "GESTION_EXTERNA"
    return "RESPUESTA_DIRECTA"