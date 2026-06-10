from pydantic import BaseModel, EmailStr
from typing import Optional


# ── LOGIN ──────────────────────────────────────────────────

class LoginInput(BaseModel):
    """Credenciales para iniciar sesión."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Respuesta al iniciar sesión exitosamente."""
    access_token: str
    token_type: str = "bearer"
    usuario: dict  # datos básicos del usuario (id, email, rol)


# ── REGISTRO ───────────────────────────────────────────────

class RegistroInput(BaseModel):
    """Datos para crear una nueva cuenta."""
    nombre: str
    email: EmailStr
    password: str


# ── RECUPERACIÓN DE CONTRASEÑA ─────────────────────────────

class RecuperarContrasenaInput(BaseModel):
    """Email del usuario que olvidó su contraseña."""
    email: EmailStr


class VerificarCodigoInput(BaseModel):
    """Código de 6 dígitos enviado al correo."""
    email: EmailStr
    codigo: str


class NuevaContrasenaInput(BaseModel):
    """Nueva contraseña tras verificar el código."""
    email: EmailStr
    codigo: str
    nueva_password: str


# ── VERIFICACIÓN DE EMAIL ──────────────────────────────────

class VerificarEmailInput(BaseModel):
    """Token único enviado al email al registrarse."""
    token: str


class ReenviarVerificacionInput(BaseModel):
    """Email al que se reenvía el correo de verificación."""
    email: EmailStr


# ── VALIDACIÓN DE DOMINIO ──────────────────────────────────

class ValidarDominioInput(BaseModel):
    """Dominio a verificar si está en lista negra."""
    dominio: str


# ── REFRESH TOKEN ──────────────────────────────────────────

class RefreshTokenResponse(BaseModel):
    """Nuevo access token generado con el refresh token."""
    access_token: str
    token_type: str = "bearer"


# ─────────────────────────────────────────────────────────────
# admin.py  
# ─────────────────────────────────────────────────────────────

class ConfiguracionResponse(BaseModel):
    """Configuración actual del sistema."""
    nombre_sistema: Optional[str]
    max_intentos_login: Optional[int]
    duracion_sesion_minutos: Optional[int]
    email_soporte: Optional[str]


class ConfiguracionInput(BaseModel):
    """Campos a actualizar en la configuración (todos opcionales)."""
    nombre_sistema: Optional[str] = None
    max_intentos_login: Optional[int] = None
    duracion_sesion_minutos: Optional[int] = None
    email_soporte: Optional[str] = None


class RolInput(BaseModel):
    """Datos para crear un rol."""
    nombre: str
    descripcion: Optional[str] = None
    permisos: Optional[list[str]] = []


class RolResponse(BaseModel):
    """Datos de un rol existente."""
    id: int
    nombre: str
    descripcion: Optional[str]
    permisos: Optional[list[str]]


class DominioSospechosoInput(BaseModel):
    """Dominio a agregar a la lista negra."""
    dominio: str
    razon: Optional[str] = None


class DominioSospechosoResponse(BaseModel):
    """Datos de un dominio sospechoso."""
    dominio: str
    razon: Optional[str]
