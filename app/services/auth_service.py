# Contiene toda la lógica de negocio de autenticación
# ─────────────────────────────────────────────────────────────

import secrets
import string

from app.repositories.user_repo import (
    get_user_by_email,
    create_user,
    update_user,              # necesitarás agregar esta función a tu repo
    get_user_by_token,        # necesitarás agregar esta función a tu repo
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

def register_user(user_data):
    print(">>> 1. Iniciando registro")
    existing_user = get_user_by_email(user_data.email)
    print(">>> 2. Verificó email existente")
    if existing_user:
        return None

    user_dict = user_data.dict()
    user_dict["password"] = hash_password(user_dict["password"])
    user_dict["verificado"] = False
    user_dict["token_verificacion"] = _generar_token()
    print(">>> 3. Datos preparados, intentando crear usuario")

    create_user(user_dict)
    print(">>> 4. Usuario creado exitosamente")

    return True

# ── HELPERS INTERNOS ───────────────────────────────────────

def _generar_codigo(longitud: int = 6) -> str:
    """Genera un código numérico aleatorio (para recuperación de contraseña)."""
    return "".join(secrets.choice(string.digits) for _ in range(longitud))


def _generar_token() -> str:
    """Genera un token URL-safe aleatorio (para verificación de email)."""
    return secrets.token_urlsafe(32)


# ── REGISTRO ───────────────────────────────────────────────

def register_user(user_data):
    """
    Registra un nuevo usuario.
    - Verifica que el email no esté en uso
    - Hashea la contraseña
    - Genera token de verificación de email
    - Retorna None si el email ya existe
    """
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        return None  # el email ya está registrado

    user_dict = user_data.dict()
    user_dict["password"] = hash_password(user_dict["password"])
    user_dict["verificado"] = False
    user_dict["token_verificacion"] = _generar_token()

    create_user(user_dict)

    # TODO: enviar email con el token de verificación
    # send_verification_email(user_dict["email"], user_dict["token_verificacion"])

    return True


# ── LOGIN ──────────────────────────────────────────────────

def login_user(email: str, password: str):
    """
    Autentica un usuario con email y contraseña.
    - Verifica que el usuario exista y esté activo
    - Verifica que el email haya sido verificado
    - Compara la contraseña con el hash almacenado
    - Retorna access_token y refresh_token si todo es correcto
    """
    user = get_user_by_email(email)

    if not user:
        return None  # usuario no encontrado

    if not user.get("activo", True):
        return "inactivo"  # cuenta desactivada

    if not user.get("verificado", False):
        return "no_verificado"  # email sin verificar

    if not verify_password(password, user["password"]):
        return None  # contraseña incorrecta

    token_data = {
        "sub": user["email"],
        "rol": user.get("rol", "usuario")
    }

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
       "usuario": {
    "id": user["id_user"],  # ← cambiar "id" por "id_user"
    "email": user["email"],
    "nombre": user.get("nombre"),
    "rol": user.get("rol", "usuario")
}
    }


# ── CERRAR SESIÓN ──────────────────────────────────────────

def logout_user(token: str):
    """
    Cierra la sesión del usuario.
    NOTA: JWT es stateless, para invalidar tokens debes mantener
    una blacklist en base de datos o Redis.
    Por ahora retorna True (el cliente debe eliminar el token).
    """
    # TODO: agregar token a blacklist en BD
    return True


def logout_all_sessions(email: str):
    """
    Cierra todas las sesiones del usuario (invalida todos sus tokens).
    Implementar rotando el SECRET_KEY por usuario o guardando versión de token en BD.
    """
    # TODO: actualizar "token_version" del usuario en BD para invalidar todos sus tokens
    return True


# ── RECUPERACIÓN DE CONTRASEÑA ─────────────────────────────

def recuperar_contrasena(email: str):
    """
    Inicia el flujo de recuperación de contraseña.
    - Genera un código de 6 dígitos
    - Lo guarda en el usuario
    - Envía el código por email
    Retorna False si el email no existe.
    """
    user = get_user_by_email(email)
    if not user:
        return False

    codigo = _generar_codigo()
    update_user(email, {"codigo_recuperacion": codigo})

    # TODO: enviar email con el código
    # send_recovery_email(email, codigo)

    return True


def verificar_codigo_recuperacion(email: str, codigo: str):
    """
    Verifica que el código de recuperación sea válido.
    Retorna False si el usuario no existe o el código no coincide.
    """
    user = get_user_by_email(email)
    if not user:
        return False

    if user.get("codigo_recuperacion") != codigo:
        return False  # código incorrecto

    return True


def cambiar_contrasena(email: str, codigo: str, nueva_password: str):
    """
    Cambia la contraseña tras verificar el código.
    - Verifica el código nuevamente
    - Hashea la nueva contraseña
    - Borra el código de recuperación para que no se reutilice
    """
    if not verificar_codigo_recuperacion(email, codigo):
        return False

    update_user(email, {
        "password": hash_password(nueva_password),
        "codigo_recuperacion": None  # invalida el código usado
    })

    return True


# ── VERIFICACIÓN DE EMAIL ──────────────────────────────────

def verificar_email(token: str):
    """
    Marca el email del usuario como verificado.
    - Busca al usuario por su token de verificación
    - Actualiza 'verificado' a True y borra el token
    Retorna False si el token no es válido.
    """
    user = get_user_by_token(token)  # busca por token_verificacion
    if not user:
        return False

    update_user(user["email"], {
        "verificado": True,
        "token_verificacion": None  # borra el token para que no se reutilice
    })

    return True


def reenviar_verificacion(email: str):
    """
    Genera un nuevo token de verificación y lo envía por email.
    Retorna False si el usuario no existe o ya verificó su email.
    """
    user = get_user_by_email(email)
    if not user:
        return False

    if user.get("verificado"):
        return "ya_verificado"

    nuevo_token = _generar_token()
    update_user(email, {"token_verificacion": nuevo_token})

    # TODO: enviar email con el nuevo token
    # send_verification_email(email, nuevo_token)

    return True


# ── VALIDACIÓN DE DOMINIO ──────────────────────────────────

def validar_dominio(dominio: str):
    """
    Verifica si un dominio está en la lista negra.
    Se usa antes del registro para bloquear dominios sospechosos.
    Retorna True si el dominio es seguro, False si está bloqueado.
    """
    from app.repositories.admin_repo import get_dominio_sospechoso
    resultado = get_dominio_sospechoso(dominio)
    return resultado is None  # None = no está en lista negra = seguro


# ── REFRESH TOKEN ──────────────────────────────────────────

def refrescar_token(refresh_token: str):
    """
    Genera un nuevo access token usando el refresh token.
    - Decodifica y valida el refresh token
    - Genera un nuevo access token con los mismos datos
    Retorna None si el refresh token es inválido.
    """
    try:
        payload = decode_token(refresh_token, tipo="refresh")
    except Exception:
        return None

    nuevo_token = create_access_token({
        "sub": payload.get("sub"),
        "rol": payload.get("rol", "usuario")
    })

    return nuevo_token
