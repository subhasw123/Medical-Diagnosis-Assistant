from database.db import get_connection
from werkzeug.security import check_password_hash, generate_password_hash


def create_user(full_name, email, age, gender, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (full_name, email, age, gender, password_hash)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                full_name,
                email.lower(),
                age,
                gender,
                generate_password_hash(password),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email.lower(),),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def authenticate_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, full_name, email, age, gender FROM users WHERE user_id = %s",
            (user_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
