from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    document_number: str
    document_type_id: int
    gender: str
    id_status: int
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str