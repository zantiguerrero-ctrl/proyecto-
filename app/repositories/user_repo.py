from app.core.database import get_connection

# Obtener usuario por email
def get_user_by_email(email: str):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM users
        WHERE email = %s
    """

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    conn.close()

    return user

# Crear usuario
def create_user(email: str, password: str):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        INSERT INTO users(email, password)
        VALUES(%s, %s)
    """

    cursor.execute(query, (email, password))

    conn.commit()

    conn.close()

# Obtener todos los usuarios
def get_all_users():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users"

    cursor.execute(query)

    users = cursor.fetchall()

    conn.close()

    return users

# Obtener usuario por ID
def get_user_by_id(user_id: int):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM users
        WHERE id = %s
    """

    cursor.execute(query, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user