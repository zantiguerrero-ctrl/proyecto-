from app.core.database import get_connection

def get_user_by_email(email: str):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM user WHERE email = %s"

    cursor.execute(query, (email,))
    user = cursor.fetchone()

    conn.close()

    return user


def create_user(data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO user(
            name,
            email,
            phone,
            document_number,
            document_type_id,
            gender,
            id_status,
            password
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["name"],
        data["email"],
        data["phone"],
        data["document_number"],
        data["document_type_id"],
        data["gender"],
        data["id_status"],
        data["password"]
    )

    cursor.execute(query, values)

    conn.commit()
    conn.close()