from fastapi import APIRouter

from app.api.routes import auth
from app.api.routes import users
from app.api.routes import chatbot
from app.api.routes import crisis

router = APIRouter()

router.include_router(
    auth.router,
    prefix="/auth",
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