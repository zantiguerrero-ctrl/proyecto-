from passlib.context import CryptContext
from jose import JWTError, jwt  # Captura errores relacionados con JWT (token inválido, expirado o mal formado)
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status  # Importa herramientas de FastAPI para dependencias, manejo de errores HTTP y códigos de estado
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # Importa el sistema de autenticación Bearer y las credenciales del token enviado por el usuario


from app.core.config import settings

pwd_context = CryptContext(

    schemes=["bcrypt"],
    deprecated="auto"
)
# Esquema Bearer: lee el token del header "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer()

# ── CONTRASEÑAS ────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Convierte una contraseña en texto plano a hash bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña ingresada con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)


# ── ACCESS TOKEN (corta duración: 1 hora) ──────────────────

def create_access_token(data: dict) -> str:
    """
    Crea un JWT de acceso.
    Expira en 1 hora (configurable en settings).
    data debe incluir {"sub": email_del_usuario}
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ── REFRESH TOKEN (larga duración: 7 días) ─────────────────

def create_refresh_token(data: dict) -> str:
    """
    Crea un JWT de refresco.
    Expira en 7 días. Se usa para generar nuevos access tokens
    sin que el usuario tenga que volver a iniciar sesión.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ── DECODIFICAR TOKEN ──────────────────────────────────────

def decode_token(token: str, tipo: str = "access") -> dict:
    """
    Decodifica y valida un JWT.
    Lanza 401 si el token es inválido, expirado o del tipo incorrecto.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Verifica que sea el tipo correcto (access o refresh)
        if payload.get("type") != tipo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token incorrecto"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )


# ── DEPENDENCIAS FASTAPI ───────────────────────────────────

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """
    Dependencia de FastAPI para proteger rutas.
    Uso: @router.get("/ruta") def ruta(usuario = Depends(get_current_user))
    Extrae el token del header, lo valida y retorna el payload.
    """
    token = credentials.credentials
    payload = decode_token(token, tipo="access")

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin información de usuario"
        )

    return payload  # contiene: {"sub": email, "exp": ..., "type": "access"}


def verify_admin(usuario: dict = Depends(get_current_user)) -> dict:
    """
    Dependencia para rutas exclusivas de administrador.
    Uso: @router.get("/admin/ruta") def ruta(admin = Depends(verify_admin))
    Lanza 403 si el usuario autenticado no tiene rol 'admin'.
    """
    if usuario.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a administradores"
        )
    return usuario
