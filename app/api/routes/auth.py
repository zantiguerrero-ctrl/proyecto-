from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.auth import (
    LoginInput,
    RegistroInput,
    RecuperarContrasenaInput,
    VerificarCodigoInput,
    NuevaContrasenaInput,
    VerificarEmailInput,
    ReenviarVerificacionInput,
    ValidarDominioInput,
)

from app.services.auth_service import (
    login_user,
    register_user,
    logout_user,
    logout_all_sessions,
    recuperar_contrasena,
    verificar_codigo_recuperacion,
    cambiar_contrasena,
    verificar_email,
    reenviar_verificacion,
    validar_dominio,
    refrescar_token,
)

from app.core.security import get_current_user

router = APIRouter(prefix="/autenticacion", tags=["Autenticación"])
bearer_scheme = HTTPBearer()


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/registrar
# Crea una nueva cuenta de usuario
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
# POST /autenticacion/registrar
# Crea una nueva cuenta de usuario
# ─────────────────────────────────────────────────────────────
@router.post("/registrar")
def registrar(datos: RegistroInput):
    """
    Crea una nueva cuenta de usuario.
    Envía un email de verificación al registrarse.
    """
    resultado = register_user(datos)

    if resultado == "email_existente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta con este email"
        )

    if resultado == "dominio_bloqueado":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este dominio no está permitido para el registro"
        )

    return {"mensaje": "Cuenta creada. Revisa tu email para verificarla."}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/iniciar-sesion
# Autentica al usuario y retorna los tokens JWT
# ─────────────────────────────────────────────────────────────
@router.post("/iniciar-sesion")
def iniciar_sesion(credenciales: LoginInput):
    """
    Inicia sesión con email y contraseña.
    Retorna access_token (1h) y refresh_token (7 días).
    """
    resultado = login_user(credenciales.email, credenciales.password)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    if resultado == "inactivo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta cuenta ha sido desactivada"
        )

    if resultado == "no_verificado":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes verificar tu email antes de iniciar sesión"
        )

    return {
        "access_token": resultado["access_token"],
        "refresh_token": resultado["refresh_token"],
        "token_type": "bearer",
        "usuario": resultado["usuario"]
    }


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/cerrar-sesion
# Cierra la sesión actual del usuario
# ─────────────────────────────────────────────────────────────
@router.post("/cerrar-sesion")
def cerrar_sesion(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """
    Cierra la sesión del usuario invalidando su token actual.
    Requiere enviar el token en el header: Authorization: Bearer <token>
    """
    token = credentials.credentials
    logout_user(token)

    return {"mensaje": "Sesión cerrada correctamente"}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/cerrar-sesion/todos
# Cierra TODAS las sesiones activas del usuario
# ─────────────────────────────────────────────────────────────
@router.post("/cerrar-sesion/todos")
def cerrar_todas_sesiones(
    usuario_actual: dict = Depends(get_current_user)
):
    """
    Invalida todos los tokens del usuario autenticado.
    Útil cuando se sospecha de acceso no autorizado.
    """
    email = usuario_actual.get("sub")
    logout_all_sessions(email)

    return {"mensaje": "Todas las sesiones han sido cerradas"}


# ─────────────────────────────────────────────────────────────
# GET /autenticacion/yo
# Retorna los datos del usuario autenticado actualmente
# ─────────────────────────────────────────────────────────────
@router.get("/yo")
def obtener_usuario_actual(
    usuario_actual: dict = Depends(get_current_user)
):
    """
    Retorna la información del usuario dueño del token JWT.
    Requiere token válido en el header Authorization.
    """
    return {
        "email": usuario_actual.get("sub"),
        "rol": usuario_actual.get("rol", "usuario")
    }


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/recuperar-contrasena
# Inicia el flujo de recuperación enviando un código al email
# ─────────────────────────────────────────────────────────────
@router.post("/recuperar-contrasena")
def recuperar_password(datos: RecuperarContrasenaInput):
    """
    Envía un código de 6 dígitos al email del usuario.
    Por seguridad, siempre retorna el mismo mensaje aunque
    el email no exista (evita enumerar cuentas).
    """
    recuperar_contrasena(datos.email)

    # Siempre retorna éxito para no revelar si el email existe
    return {"mensaje": "Si el email existe, recibirás un código de recuperación"}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/verificar-codigo
# Verifica que el código de recuperación sea válido
# ─────────────────────────────────────────────────────────────
@router.post("/verificar-codigo")
def verificar_codigo(datos: VerificarCodigoInput):
    """
    Valida el código de 6 dígitos enviado al email.
    Debe llamarse antes de /nueva-contrasena.
    """
    valido = verificar_codigo_recuperacion(datos.email, datos.codigo)

    if not valido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código incorrecto o expirado"
        )

    return {"mensaje": "Código válido. Puedes cambiar tu contraseña."}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/nueva-contrasena
# Establece la nueva contraseña tras verificar el código
# ─────────────────────────────────────────────────────────────
@router.post("/nueva-contrasena")
def nueva_contrasena(datos: NuevaContrasenaInput):
    """
    Cambia la contraseña del usuario.
    Requiere el código de recuperación válido.
    El código se invalida después de usarse.
    """
    resultado = cambiar_contrasena(datos.email, datos.codigo, datos.nueva_password)

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código incorrecto o expirado"
        )

    return {"mensaje": "Contraseña actualizada correctamente"}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/verificar-email
# Verifica el email del usuario con el token recibido
# ─────────────────────────────────────────────────────────────
@router.post("/verificar-email")
def verificar_email_usuario(datos: VerificarEmailInput):
    """
    Activa la cuenta del usuario verificando el token de email.
    El token se envía al registrarse y se invalida al usarse.
    """
    resultado = verificar_email(datos.token)

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de verificación inválido o ya utilizado"
        )

    return {"mensaje": "Email verificado. Ya puedes iniciar sesión."}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/reenviar-verificacion
# Reenvía el email de verificación al usuario
# ─────────────────────────────────────────────────────────────
@router.post("/reenviar-verificacion")
def reenviar_email_verificacion(datos: ReenviarVerificacionInput):
    """
    Genera un nuevo token y reenvía el email de verificación.
    Útil si el correo anterior expiró o no llegó.
    """
    resultado = reenviar_verificacion(datos.email)

    if resultado is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe una cuenta con este email"
        )

    if resultado == "ya_verificado":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email ya fue verificado"
        )

    return {"mensaje": "Email de verificación reenviado"}


# ─────────────────────────────────────────────────────────────
# POST /autenticacion/validar-dominio
# Verifica si un dominio está en la lista negra
# ─────────────────────────────────────────────────────────────
@router.post("/validar-dominio")
def validar_dominio_email(datos: ValidarDominioInput):
    """
    Comprueba si un dominio está bloqueado.
    Se usa en el frontend antes del registro para validar el email.
    """
    es_seguro = validar_dominio(datos.dominio)

    if not es_seguro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este dominio no está permitido para el registro"
        )

    return {"mensaje": "Dominio válido", "permitido": True}


# ─────────────────────────────────────────────────────────────
# GET /autenticacion/tokens/refrescar
# Genera un nuevo access token usando el refresh token
# ─────────────────────────────────────────────────────────────
@router.get("/tokens/refrescar")
def refrescar_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """
    Renueva el access token sin necesidad de volver a hacer login.
    Enviar el REFRESH TOKEN (no el access token) en el header.
    Authorization: Bearer <refresh_token>
    """
    nuevo_token = refrescar_token(credentials.credentials)

    if not nuevo_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado. Inicia sesión nuevamente."
        )

    return {
        "access_token": nuevo_token,
        "token_type": "bearer"
    }

