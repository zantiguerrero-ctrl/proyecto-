from pydantic import BaseModel, EmailStr

# Crear usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Respuesta usuario
class UserResponse(BaseModel):
    id: int
    email: EmailStr

# Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str