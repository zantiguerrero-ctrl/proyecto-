from fastapi import APIRouter

router = APIRouter()

# Get users
@router.get("/")
def get_users():

    return {
        "message": "Lista de usuarios"
    }

# Get user by id
@router.get("/{user_id}")
def get_user(user_id: int):

    return {
        "user_id": user_id
    }
