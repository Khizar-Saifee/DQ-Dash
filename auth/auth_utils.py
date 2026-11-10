import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
DB_PATH = os.path.join(BASE_DIR, "database", "users.db")


def init_db():
    # Ensure database folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    if not username or not password:
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    hashed_pw = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_pw)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    if not username or not password:
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        stored_pw = result[0]
        return bcrypt.checkpw(password.encode(), stored_pw)

    return False