from fastapi import APIRouter, HTTPException, Depends, status

from app.schemas.auth import (
    ConfiguracionResponse,
    ConfiguracionInput,
    RolInput,
    RolResponse,
    DominioSospechosoInput,
    DominioSospechosoResponse,
)

from app.services.admin_service import (
    obtener_configuracion,
    actualizar_configuracion,
    crear_rol,
    listar_roles,
    eliminar_rol,
    listar_dominios_sospechosos,
    agregar_dominio_sospechoso,
    eliminar_dominio_sospechoso,
)

from app.core.security import verify_admin

# Todas las rutas de este router requieren ser administrador
router = APIRouter(
    prefix="/admin",
    tags=["Administración"],
    dependencies=[Depends(verify_admin)]  # protege TODAS las rutas del router
)


# ─────────────────────────────────────────────────────────────
# GET /admin/configuracion
# Obtiene la configuración actual del sistema
# ─────────────────────────────────────────────────────────────
@router.get("/configuracion", response_model=ConfiguracionResponse)
def get_configuracion():
    """
    Retorna la configuración general del sistema.
    Incluye: nombre del sistema, intentos de login, duración de sesión, etc.
    Solo accesible por administradores.
    """
    config = obtener_configuracion()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró configuración del sistema"
        )

    return config


# ─────────────────────────────────────────────────────────────
# PUT /admin/configuracion
# Actualiza la configuración del sistema
# ─────────────────────────────────────────────────────────────
@router.put("/configuracion")
def put_configuracion(datos: ConfiguracionInput):
    """
    Actualiza uno o más campos de la configuración del sistema.
    Solo se actualizan los campos enviados (no nulos).
    """
    resultado = actualizar_configuracion(datos.dict())

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron campos para actualizar"
        )

    return {"mensaje": "Configuración actualizada correctamente"}


# ─────────────────────────────────────────────────────────────
# POST /admin/roles
# Crea un nuevo rol en el sistema
# ─────────────────────────────────────────────────────────────
@router.post("/roles", status_code=status.HTTP_201_CREATED)
def post_rol(datos: RolInput):
    """
    Crea un nuevo rol con sus permisos.
    Retorna error si ya existe un rol con el mismo nombre.
    """
    resultado = crear_rol(datos.dict())

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un rol con el nombre '{datos.nombre}'"
        )

    return {"mensaje": f"Rol '{datos.nombre}' creado correctamente"}


# ─────────────────────────────────────────────────────────────
# GET /admin/roles
# Lista todos los roles del sistema
# ─────────────────────────────────────────────────────────────
@router.get("/roles", response_model=list[RolResponse])
def get_roles():
    """
    Retorna la lista completa de roles disponibles en el sistema.
    """
    return listar_roles()


# ─────────────────────────────────────────────────────────────
# DELETE /admin/roles/:id
# Elimina un rol por su ID
# ─────────────────────────────────────────────────────────────
@router.delete("/roles/{rol_id}", status_code=status.HTTP_200_OK)
def delete_rol(rol_id: int):
    """
    Elimina un rol del sistema por su ID.
    Precaución: asegúrate de que ningún usuario tenga ese rol asignado.
    """
    resultado = eliminar_rol(rol_id)

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un rol con ID {rol_id}"
        )

    return {"mensaje": f"Rol eliminado correctamente"}


# ─────────────────────────────────────────────────────────────
# GET /admin/dominios-sospechosos
# Lista todos los dominios en la lista negra
# ─────────────────────────────────────────────────────────────
@router.get("/dominios-sospechosos", response_model=list[DominioSospechosoResponse])
def get_dominios_sospechosos():
    """
    Retorna todos los dominios bloqueados para el registro.
    Estos dominios son verificados en /autenticacion/validar-dominio.
    """
    return listar_dominios_sospechosos()


# ─────────────────────────────────────────────────────────────
# POST /admin/dominios-sospechosos
# Agrega un dominio a la lista negra
# ─────────────────────────────────────────────────────────────
@router.post("/dominios-sospechosos", status_code=status.HTTP_201_CREATED)
def post_dominio_sospechoso(datos: DominioSospechosoInput):
    """
    Agrega un dominio a la lista negra del sistema.
    Ejemplo: bloquear 'tempmail.com' o 'guerrillamail.com'.
    """
    resultado = agregar_dominio_sospechoso(datos.dict())

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El dominio '{datos.dominio}' ya está en la lista negra"
        )

    return {"mensaje": f"Dominio '{datos.dominio}' agregado a la lista negra"}


# ─────────────────────────────────────────────────────────────
# DELETE /admin/dominios-sospechosos/:dominio
# Elimina un dominio de la lista negra
# ─────────────────────────────────────────────────────────────
@router.delete("/dominios-sospechosos/{dominio}")
def delete_dominio_sospechoso(dominio: str):
    """
    Elimina un dominio de la lista negra permitiendo su uso en registros.
    El parámetro dominio va en la URL: /admin/dominios-sospechosos/tempmail.com
    """
    resultado = eliminar_dominio_sospechoso(dominio)

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el dominio '{dominio}' en la lista negra"
        )

    return {"mensaje": f"Dominio '{dominio}' eliminado de la lista negra"}
