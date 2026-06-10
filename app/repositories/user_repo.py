from app.core.database import get_connection


def get_user_by_email(email: str):
    """Busca un usuario por su email. Retorna dict o None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_token(token: str):
    """Busca un usuario por su token de verificación de email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM user WHERE token_verificacion = %s", (token,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(data: dict):
    """Crea un nuevo usuario en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO user (
            name, email, phone, document_number, document_type_id,
            gender, id_status, password, nombre, rol, verificado, token_verificacion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data.get("name"),
        data["email"],
        data.get("phone"),
        data.get("document_number"),
        data.get("document_type_id"),
        data.get("gender"),
        data.get("id_status", 1),
        data["password"],
        data.get("nombre"),
        data.get("rol", "usuario"),
        data.get("verificado", False),
        data.get("token_verificacion")
    )

    cursor.execute(query, values)
    conn.commit()
    conn.close()


def update_user(email: str, datos: dict):
    """Actualiza campos del usuario identificado por email."""
    if not datos:
        return

    conn = get_connection()
    cursor = conn.cursor()

    campos = ", ".join(f"{campo} = %s" for campo in datos.keys())
    valores = list(datos.values())
    valores.append(email)

    query = f"UPDATE user SET {campos} WHERE email = %s"
    cursor.execute(query, valores)

    conn.commit()
    conn.close()