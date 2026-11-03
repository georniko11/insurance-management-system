from app.db import get_db


def get_user_by_id(user_id):
    conn = get_db()

    return conn.execute(
        """
        SELECT user_id, name, email, is_active
        FROM users
        WHERE user_id = %s
        """,
        (user_id,)
    ).fetchone()


def get_user_by_email(email):
    conn = get_db()

    return conn.execute(
        """
        SELECT user_id, name, email, password_hash, is_active
        FROM users
        WHERE email = %s
        """,
        (email,)
    ).fetchone()
