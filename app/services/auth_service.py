from app.repositories.user_repo import (
    get_user_by_email,
    create_user
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

def register_user(user_data):

    existing_user = get_user_by_email(user_data.email)

    if existing_user:
        return None

    user_dict = user_data.dict()

    user_dict["password"] = hash_password(
        user_dict["password"]
    )

    create_user(user_dict)

    return True


def login_user(email: str, password: str):

    user = get_user_by_email(email)

    if not user:
        return None

    valid_password = verify_password(
        password,
        user["password"]
    )

    if not valid_password:
        return None

    token = create_access_token({
        "sub": user["email"]
    })

    return token