from datetime import date
from app.models.schemas import SolicitudInput, SolicitudOutput
from app.companies.registry import get_company_config
from app.core.validator import validar_solicitud
from app.core.classifier import clasificar_solicitud
from app.core.router import determinar_siguiente_paso
from app.integrations.mock_platform import get_platform
from app.integrations.mensajeria_del_valle import obtener_prioridad_externa

def procesar_solicitud(solicitud: SolicitudInput) -> SolicitudOutput:
    # 1. Validar empresa parametrizada
    config = get_company_config(solicitud.compania)

    # 2. Validar información mínima
    validacion = validar_solicitud(solicitud.solicitud_descripcion)
    if not validacion.get("valida", False):
        return SolicitudOutput(
            compania=solicitud.compania,
            solicitud_id=solicitud.solicitud_id,
            solicitud_fecha=date.today(),
            proximo_paso="CIERRE_POR_INFORMACION_INSUFICIENTE",
            justificacion=validacion.get("razon", "Información incompleta o faltante."),
            estado="cerrado",
        )

    # 3. Verificar si el cliente provee prioridad externa
    prioridad_override = None
    if config.get("prioridad_externa"):
        # Necesitamos clasificar primero para conocer el tipo (llamada liviana sin prioridad)
        clasificacion_previa = clasificar_solicitud(
            solicitud.solicitud_descripcion, config["categorias"]
        )
        prioridad_override = obtener_prioridad_externa(
            clasificacion_previa.get("tipo_id_cliente", ""),
            clasificacion_previa.get("numero_id_cliente", ""),
            clasificacion_previa.get("tipo", ""),
        )

    # 4. Clasificar, priorizar y extraer datos
    clasificacion = clasificar_solicitud(
        solicitud.solicitud_descripcion,
        config["categorias"],
        prioridad_override=prioridad_override,
    )

    # 5. Determinar siguiente paso
    siguiente_paso = determinar_siguiente_paso(clasificacion["tipo"], config)

    # 6. Si es gestión externa, crear caso en plataforma
    id_plataforma = None
    estado = "pendiente" if siguiente_paso == "GESTION_EXTERNA" else "cerrado"
    if siguiente_paso == "GESTION_EXTERNA":
        platform = get_platform(config["plataforma"])
        id_plataforma = platform.crear_caso(
            solicitud_id=solicitud.solicitud_id,
            descripcion=solicitud.solicitud_descripcion,
            tipo=clasificacion["tipo"],
            prioridad=clasificacion["prioridad"],
        )

    return SolicitudOutput(
        compania=solicitud.compania,
        solicitud_id=solicitud.solicitud_id,
        solicitud_fecha=date.today(),
        solicitud_tipo=clasificacion.get("tipo"),
        solicitud_prioridad=clasificacion.get("prioridad"),
        solicitud_id_cliente=clasificacion.get("tipo_id_cliente"),
        solicitud_tipo_id_cliente=clasificacion.get("numero_id_cliente"),
        solicitud_id_plataforma_externa=id_plataforma,
        proximo_paso=siguiente_paso,
        justificacion=clasificacion.get("justificacion"),
        estado=estado,
    )