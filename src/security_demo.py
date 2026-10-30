import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db" / "database.db"


def vulnerable_login(conn, login):
    return conn.execute(f"SELECT * FROM users WHERE login = '{login}'").fetchall()


def secure_login(conn, login):
    return conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchall()


def secure_product_search(conn, text):
    return conn.execute("SELECT product_id, name FROM products WHERE name LIKE ?", (f"%{text}%",)).fetchall()


def run_demo(conn):
    payload = "' OR '1'='1"
    normal = conn.execute("SELECT login FROM users LIMIT 1").fetchone()
    if normal:
        print("Обычный логин:", normal[0], len(vulnerable_login(conn, normal[0])))
    print("Уязвимый запрос:", len(vulnerable_login(conn, payload)))
    print("Параметризованный запрос:", len(secure_login(conn, payload)))
    print("Безопасный поиск товара:", len(secure_product_search(conn, payload)))
    assert len(secure_login(conn, payload)) == 0


if __name__ == "__main__":
    with sqlite3.connect(DB) as conn:
        run_demo(conn)
