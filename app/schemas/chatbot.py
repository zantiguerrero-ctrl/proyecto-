from pydantic import BaseModel

# Mensaje usuario
class ChatMessage(BaseModel):
    message: str

# Respuesta chatbot
class ChatResponse(BaseModel):
    response: str