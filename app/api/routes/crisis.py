from fastapi import APIRouter

router = APIRouter()


# Obtener líneas de ayuda
@router.get("/lineas-de-ayuda")
def obtener_lineas_ayuda():

    return {
        "message": "Lista de líneas de ayuda"
    }


# Historial de casos críticos
@router.get("/historial-critico")
def historial_critico():

    return {
        "message": "Historial de crisis críticas"
    }