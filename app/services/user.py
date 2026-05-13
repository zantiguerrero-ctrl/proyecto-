from app.repositories.user_repo import (
    get_all_users,
    get_user_by_id
)

# Obtener usuarios
def get_users_service():

    users = get_all_users()

    return users

# Obtener usuario por ID
def get_user_service(user_id: int):

    user = get_user_by_id(user_id)

    return user