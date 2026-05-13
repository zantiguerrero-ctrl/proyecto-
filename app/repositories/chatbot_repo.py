from app.core.database import get_connection

# Guardar chat
def save_chat(message: str, response: str):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        INSERT INTO chats(message, response)
        VALUES(%s, %s)
    """

    cursor.execute(query, (message, response))

    conn.commit()

    conn.close()