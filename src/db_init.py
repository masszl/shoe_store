import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "database.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
        print("База данных успешно инициализирована")
    except (sqlite3.Error, OSError) as error:
        conn.rollback()
        print(f"Ошибка создания базы данных: {error}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
