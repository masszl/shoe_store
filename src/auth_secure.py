import hashlib
import hmac
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db" / "database.db"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def prepare_auth(conn):
    fields = {row[1] for row in conn.execute("PRAGMA table_info(users)")}
    if "password_hash" not in fields:
        conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    conn.execute("CREATE TABLE IF NOT EXISTS login_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, status TEXT NOT NULL, login_time TEXT DEFAULT (datetime('now')))")
    conn.commit()


def register_user(conn, login, password):
    prepare_auth(conn)
    role_columns = {row[1] for row in conn.execute("PRAGMA table_info(roles)")}
    role_col = "role_name" if "role_name" in role_columns else "name"
    role = conn.execute(f"SELECT role_id FROM roles WHERE {role_col} = 'reader' LIMIT 1").fetchone()
    if role is None:
        raise RuntimeError("Сначала запустите maintenance.py для создания роли reader")
    conn.execute("INSERT INTO users (last_name, first_name, login, role_id, password_hash) VALUES (?, ?, ?, ?, ?)", ("Тестовый", "Пользователь", login, role[0], hash_password(password)))
    conn.commit()


def check_password(conn, login, password):
    prepare_auth(conn)
    row = conn.execute("SELECT password_hash FROM users WHERE login = ?", (login,)).fetchone()
    valid = bool(row and row[0] and hmac.compare_digest(row[0], hash_password(password)))
    conn.execute("INSERT INTO login_audit (login, status) VALUES (?, ?)", (login, "успех" if valid else "отказ"))
    conn.commit()
    return valid


if __name__ == "__main__":
    with sqlite3.connect(DB) as conn:
        prepare_auth(conn)
        print("Поле password_hash и журнал login_audit готовы")
