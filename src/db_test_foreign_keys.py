import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "db" / "database_day3_test.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        conn.execute(
            "INSERT INTO orders (user_id) VALUES (?)",
            (999999,)
        )
        print("[FAIL] Заказ с несуществующим пользователем создан")
        conn.rollback()

    except sqlite3.IntegrityError:
        print("[PASS] Внешний ключ работает: заказ отклонён")
        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
