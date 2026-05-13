from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate
from app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter()

# Register
@router.post("/register")
def register(user: UserCreate):

    result = register_user(
        user.email,
        user.password
    )

    if not result:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return {
        "message": "User created"
    }

# Login
@router.post("/login")
def login(user: UserCreate):

    token = login_user(
        user.email,
        user.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token
    }
