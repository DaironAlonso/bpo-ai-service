# Simulación del microservicio externo de MENSAJERIA DEL VALLE
# En producción este sería un httpx.get/post a su endpoint real

def obtener_prioridad_externa(tipo_documento: str, numero_documento: str, tipo_solicitud: str) -> str:
    """
    Simula llamada al microservicio externo del cliente.
    Retorna prioridad: Alta, Media o Baja.
    """
    # Lógica simulada: fraudes y paquetes perdidos siempre Alta
    if tipo_solicitud in ["Paquete perdido", "Fraude"]:
        return "Alta"
    if tipo_documento == "NIT":
        return "Alta"  # Clientes corporativos tienen prioridad alta
    return "Media"