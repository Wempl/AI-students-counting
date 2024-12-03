import sqlite3
import hashlib
import os


DATABASE_PATH = "users.db"


def init_db():
    """
    Инициализация базы данных. Создаёт таблицу 'users', если она отсутствует.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            photo_path TEXT DEFAULT NULL
        )
    """)
    conn.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Существующие таблицы:", tables)  

    conn.close()


def hash_password(password):
    """
    Хэширует пароль с использованием SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """
    Регистрирует нового пользователя.
    Возвращает True, если регистрация успешна.
    Возвращает False, если пользователь с таким именем уже существует.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Таблицы в базе данных:", tables)

        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        conn.close()
        print("Пользователь успешно зарегистрирован.")
        return True
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким именем уже существует.")
        return False
    except sqlite3.OperationalError as e:
        print(f"Ошибка работы с базой данных: {e}")
        return False


def authenticate_user(username, password):
    """
    Аутентификация пользователя. Проверяет имя пользователя и пароль.
    Возвращает True, если аутентификация успешна.
    Возвращает False, если данные неверны.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        password_hash = hash_password(password)
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            print("Аутентификация успешна.")
            return True
        else:
            print("Ошибка аутентификации: Неверное имя пользователя или пароль.")
            return False
    except sqlite3.OperationalError as e:
        print(f"Ошибка работы с базой данных: {e}")
        return False


def get_all_users():
    """
    Получает список всех пользователей из базы данных.
    Возвращает список словарей с информацией о пользователях.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, photo_path FROM users")
        users = cursor.fetchall()
        conn.close()

        user_list = [
            {"id": user[0], "username": user[1], "photo_path": user[2]} for user in users
        ]
        return user_list
    except sqlite3.OperationalError as e:
        print(f"Ошибка работы с базой данных: {e}")
        return []


if __name__ == "__main__":
    init_db()

    print("Регистрация пользователя...")
    if register_user("test_user", "secure_password"):
        print("Пользователь зарегистрирован.")
    else:
        print("Ошибка: Пользователь с таким именем уже существует.")

    print("\nАутентификация пользователя...")
    if authenticate_user("test_user", "secure_password"):
        print("Аутентификация успешна.")
    else:
        print("Ошибка аутентификации.")

    print("\nСписок пользователей:")
    for user in get_all_users():
        print(user)
