from fastapi import APIRouter

from app.api.routes import auth
from app.api.routes import users
from app.api.routes import chatbot
from app.api.routes import crisis
from app.api.routes import admin  # Importa las rutas del módulo admin para integrarlas y utilizarlas en la aplicación

router = APIRouter()

router.include_router(
    auth.router,
    tags=["Auth"]
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

router.include_router(
    chatbot.router,
    prefix="/chatbot",
    tags=["Chatbot"]
)

router.include_router(
    crisis.router,
    prefix="/crisis",
    tags=["Crisis"]
)
 # Agrega las rutas del módulo admin con el prefijo "/admin" y las etiqueta como "Admin"
router.include_router(
    admin.router,
     prefix="/admin",
     tags=["Admin"]
     )