import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "database_day3_relations_test.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        conn.execute("INSERT INTO orders (user_id) VALUES (999999)")
        print("[FAIL] FOREIGN KEY")
    except sqlite3.IntegrityError:
        print("[PASS] FOREIGN KEY")
        conn.rollback()

    conn.execute("INSERT INTO roles (role_name) VALUES ('Покупатель')")
    role_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO users (last_name, first_name, login, role_id) VALUES (?, ?, ?, ?)", ("Иванов", "Иван", "ivan123", role_id))
    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO sizes (size_value) VALUES (42)")
    size_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO products (category, subcategory, manufacturer, name, image_path, price) VALUES (?, ?, ?, ?, ?, ?)", ("Обувь", "Кроссовки", "Nike", "Air Max", "nike.jpg", 5000))
    product_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO stock_items (product_id, size_id, quantity) VALUES (?, ?, ?)", (product_id, size_id, 5))
    stock_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO orders (user_id) VALUES (?)", (user_id,))
    order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, stock_id, 1, 5000))

    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        print("[FAIL] RESTRICT")
    except sqlite3.IntegrityError:
        print("[PASS] RESTRICT")

    conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    remaining = conn.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (order_id,)).fetchone()[0]
    print("[PASS] CASCADE" if remaining == 0 else "[FAIL] CASCADE")

    index_count = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'index' AND name LIKE 'idx_%'").fetchone()[0]
    print(f"[PASS] Индексы: {index_count}/9" if index_count == 9 else f"[FAIL] Индексы: {index_count}/9")
    conn.rollback()
    conn.close()


if __name__ == "__main__":
    main()
