
import sqlite3
import hashlib
import os

DB_PATH = "users.db"


def create_database():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(username, password):
    username = username.strip()

    if not username or not password:
        return False, "Please fill in all fields."

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )

        connection.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    finally:
        connection.close()


def login(username, password):
    connection = sqlite3.connect(DB_PATH)

    user = connection.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username.strip(), hash_password(password))
    ).fetchone()

    connection.close()

    return user is not None


create_database()
