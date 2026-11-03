from werkzeug.security import check_password_hash
from app.auth.queries import get_user_by_email


def authenticate_user(email, password):
    user_data = get_user_by_email(email)

    if user_data is None:
        return None

    if not user_data["is_active"]:
        return None

    if not check_password_hash(user_data["password_hash"], password):
        return None

    return user_data
