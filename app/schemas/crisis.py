from pydantic import BaseModel

class CrisisAlert(BaseModel):
    user_id: int
    level: str
    description: str

class CrisisResponse(BaseModel):
    message: str
    status: str