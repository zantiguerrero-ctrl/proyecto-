from fastapi import APIRouter

router = APIRouter()


# Enviar mensaje al chatbot
@router.post("/mensaje")
def enviar_mensaje():

    return {
        "message": "Mensaje enviado al chatbot"
    }


# Obtener historial del usuario
@router.get("/historial/{idUsuario}")
def obtener_historial(idUsuario: int):

    return {
        "message": f"Historial del usuario {idUsuario}"
    }


# Eliminar sesión de chat
@router.delete("/sesion/{id}")
def eliminar_sesion(id: int):

    return {
        "message": f"Sesión {id} eliminada"
    }


# Detectar crisis emocional
@router.post("/detectar-crisis")
def detectar_crisis():

    return {
        "message": "Análisis de crisis realizado"
    }


# Obtener riesgo de una sesión
@router.get("/riesgo/{idSesion}")
def obtener_riesgo(idSesion: int):

    return {
        "message": f"Nivel de riesgo de la sesión {idSesion}"
    }


# Escalar caso crítico
@router.post("/escalar")
def escalar_caso():

    return {
        "message": "Caso escalado correctamente"
    }