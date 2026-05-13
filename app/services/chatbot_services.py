# Respuesta chatbot
def chatbot_response(message: str):

    message = message.lower()

    if "hola" in message:
        return "Hola, ¿cómo estás?"

    if "ayuda" in message:
        return "Estoy aquí para ayudarte."

    return "No entendí tu mensaje."