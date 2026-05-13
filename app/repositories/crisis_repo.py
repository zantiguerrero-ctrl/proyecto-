from app.core.database import get_connection

# Crear alerta
def create_crisis_alert(
    user_id: int,
    level: str,
    description: str
):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        INSERT INTO crisis_alerts(
            user_id,
            level,
            description
        )
        VALUES(%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            user_id,
            level,
            description
        )
    )

    conn.commit()

    conn.close()