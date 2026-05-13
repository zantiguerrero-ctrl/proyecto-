from app.repositories.user_repo import (
    get_user_by_email,
    create_user
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

# Register
def register_user(email: str, password: str):

    existing_user = get_user_by_email(email)

    if existing_user:
        return None

    hashed_password = hash_password(password)

    create_user(
        email,
        hashed_password
    )

    return True

# Login
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