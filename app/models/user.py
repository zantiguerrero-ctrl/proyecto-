class User:

    def __init__(
        self,
        id: int,
        email: str,
        password: str,
        nombre: str = None,
        rol: str = "usuario",           # "usuario" | "admin"
        verificado: bool = False,       # True cuando verifica su email
        activo: bool = True,            # False si fue desactivado
        token_verificacion: str = None, # Token enviado al email
        codigo_recuperacion: str = None # Código de recuperación de contraseña
    ):

        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre
        self.rol = rol
        self.verificado = verificado
        self.activo = activo
        self.token_verificacion = token_verificacion
        self.codigo_recuperacion = codigo_recuperacion

    def to_dict(self):

        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "rol": self.rol,
            "verificado": self.verificado,
            "activo": self.activo
        }


# ─────────────────────────────────────────────────────────────
# rol.py  →  
# ─────────────────────────────────────────────────────────────

class Rol:

    def __init__(
        self,
        id: int,
        nombre: str,
        descripcion: str = None,
        permisos: list = None
    ):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.permisos = permisos or []

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "permisos": self.permisos
        }


# ─────────────────────────────────────────────────────────────
# configuracion.py  
# ─────────────────────────────────────────────────────────────

class Configuracion:

    def __init__(
        self,
        id: int,
        nombre_sistema: str = None,
        max_intentos_login: int = 5,
        duracion_sesion_minutos: int = 60,
        email_soporte: str = None
    ):
        self.id = id
        self.nombre_sistema = nombre_sistema
        self.max_intentos_login = max_intentos_login
        self.duracion_sesion_minutos = duracion_sesion_minutos
        self.email_soporte = email_soporte

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_sistema": self.nombre_sistema,
            "max_intentos_login": self.max_intentos_login,
            "duracion_sesion_minutos": self.duracion_sesion_minutos,
            "email_soporte": self.email_soporte
        }


# ─────────────────────────────────────────────────────────────
# dominio_sospechoso.py  
# ─────────────────────────────────────────────────────────────

class DominioSospechoso:

    def __init__(
        self,
        dominio: str,
        razon: str = None
    ):
        self.dominio = dominio
        self.razon = razon

    def to_dict(self):
        return {
            "dominio": self.dominio,
            "razon": self.razon
        }

        