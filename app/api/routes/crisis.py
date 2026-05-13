from fastapi import APIRouter

router = APIRouter()

# Crisis alert
@router.post("/")
def crisis_alert():

    return {
        "message": "Alerta de crisis enviada"
    }
