from fastapi import APIRouter

router = APIRouter()

# Chat
@router.post("/")
def chat():

    return {
        "message": "Respuesta chatbot"
    }
