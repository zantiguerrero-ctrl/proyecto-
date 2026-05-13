# Detectar crisis
def detect_crisis(level: str):

    if level.lower() == "alta":

        return {
            "status": "urgent",
            "message": "Alerta enviada"
        }

    return {
        "status": "normal",
        "message": "Seguimiento recomendado"
    }