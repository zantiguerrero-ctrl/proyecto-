from app.repositories.admin_repo import (
    get_configuracion,
    update_configuracion,
    create_rol,
    get_roles,
    delete_rol,
    get_dominios_sospechosos,
    create_dominio_sospechoso,
    delete_dominio_sospechoso,
)


# ── CONFIGURACIÓN ──────────────────────────────────────────

def obtener_configuracion():
    """Retorna la configuración actual del sistema."""
    return get_configuracion()


def actualizar_configuracion(datos: dict):
    """
    Actualiza los campos de configuración del sistema.
    Solo actualiza los campos que se envíen (no nulos).
    """
    campos_a_actualizar = {k: v for k, v in datos.items() if v is not None}
    if not campos_a_actualizar:
        return False  # nada que actualizar

    update_configuracion(campos_a_actualizar)
    return True


# ── ROLES ──────────────────────────────────────────────────

def crear_rol(datos: dict):
    """
    Crea un nuevo rol en el sistema.
    Retorna None si ya existe un rol con ese nombre.
    """
    roles_existentes = get_roles()
    nombres = [r["nombre"] for r in roles_existentes]

    if datos["nombre"] in nombres:
        return None  # rol duplicado

    create_rol(datos)
    return True


def listar_roles():
    """Retorna todos los roles del sistema."""
    return get_roles()


def eliminar_rol(rol_id: int):
    """
    Elimina un rol por su ID.
    Retorna False si no existe.
    """
    resultado = delete_rol(rol_id)
    return resultado


# ── DOMINIOS SOSPECHOSOS ───────────────────────────────────

def listar_dominios_sospechosos():
    """Retorna todos los dominios en lista negra."""
    return get_dominios_sospechosos()


def agregar_dominio_sospechoso(datos: dict):
    """
    Agrega un dominio a la lista negra.
    Retorna None si el dominio ya está registrado.
    """
    dominios = get_dominios_sospechosos()
    existentes = [d["dominio"] for d in dominios]

    if datos["dominio"] in existentes:
        return None  # ya está en lista negra

    create_dominio_sospechoso(datos)
    return True


def eliminar_dominio_sospechoso(dominio: str):
    """
    Elimina un dominio de la lista negra.
    Retorna False si no existe.
    """
    return delete_dominio_sospechoso(dominio)
