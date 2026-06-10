# Acceso a base de datos para el módulo de administración
# ─────────────────────────────────────────────────────────────
import json
from app.core.database import get_connection


# ── CONFIGURACIÓN ──────────────────────────────────────────

def get_configuracion():
    """
    Retorna la configuración del sistema (siempre es una sola fila con id=1).
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM configuracion WHERE id = 1")
    config = cursor.fetchone()
    conn.close()
    return config


def update_configuracion(datos: dict):
    """
    Actualiza los campos de configuración que se pasen.
    Solo modifica los campos enviados, no toca los demás.
    """
    conn = get_connection()
    cursor = conn.cursor()

    campos = ", ".join(f"{campo} = %s" for campo in datos.keys())
    valores = list(datos.values())

    query = f"UPDATE configuracion SET {campos} WHERE id = 1"
    cursor.execute(query, valores)

    conn.commit()
    conn.close()


# ── ROLES ──────────────────────────────────────────────────

def get_roles():
    """Retorna todos los roles del sistema."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rol")
    roles = cursor.fetchall()
    conn.close()

    # Convierte el campo permisos de JSON string a lista Python
    for rol in roles:
        if rol.get("permisos") and isinstance(rol["permisos"], str):
            rol["permisos"] = json.loads(rol["permisos"])

    return roles


def create_rol(datos: dict):
    """Crea un nuevo rol en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()

    # Convierte la lista de permisos a JSON string para guardar en BD
    permisos_json = json.dumps(datos.get("permisos", []))

    query = """
        INSERT INTO rol (nombre, descripcion, permisos)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (
        datos["nombre"],
        datos.get("descripcion"),
        permisos_json
    ))

    conn.commit()
    conn.close()


def delete_rol(rol_id: int) -> bool:
    """
    Elimina un rol por ID.
    Retorna True si se eliminó, False si no existía.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rol WHERE id_rol = %s", (rol_id,))
    eliminado = cursor.rowcount > 0  # rowcount = filas afectadas

    conn.commit()
    conn.close()
    return eliminado


# ── DOMINIOS SOSPECHOSOS ───────────────────────────────────

def get_dominios_sospechosos():
    """Retorna todos los dominios en lista negra."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dominio_sospechoso")
    dominios = cursor.fetchall()
    conn.close()
    return dominios


def get_dominio_sospechoso(dominio: str):
    """
    Busca un dominio específico en la lista negra.
    Retorna el registro si existe, None si no está bloqueado.
    Se usa en /autenticacion/validar-dominio.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM dominio_sospechoso WHERE dominio = %s", (dominio,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def create_dominio_sospechoso(datos: dict):
    """Agrega un dominio a la lista negra."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO dominio_sospechoso (dominio, razon) VALUES (%s, %s)"
    cursor.execute(query, (datos["dominio"], datos.get("razon")))

    conn.commit()
    conn.close()


def delete_dominio_sospechoso(dominio: str) -> bool:
    """
    Elimina un dominio de la lista negra.
    Retorna True si se eliminó, False si no existía.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM dominio_sospechoso WHERE dominio = %s", (dominio,)
    )
    eliminado = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return eliminado
