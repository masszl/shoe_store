import sqlite3
import shutil
from pathlib import Path
from app_functions import place_order, cancel_order

root = Path(__file__).resolve().parent.parent
source = root / "db" / "database.db"
test_db = root / "db" / "database_orders_test.db"

if not source.exists():
    raise FileNotFoundError(source)

with sqlite3.connect(source) as original:
    with sqlite3.connect(test_db) as backup:
        original.backup(backup)

conn = sqlite3.connect(test_db)
conn.execute("PRAGMA foreign_keys = ON")

try:
    data = conn.execute("""
        SELECT u.user_id, si.product_id, si.size_id,
               si.stock_item_id, si.quantity
        FROM users u
        CROSS JOIN stock_items si
        WHERE si.quantity > 0
        LIMIT 1
    """).fetchone()

    if not data:
        print("Нет пользователя или товара с положительным остатком")
    else:
        user_id, product_id, size_id, stock_id, initial = data

        result = place_order(conn, user_id, product_id, size_id, 1)
        print("Создание заказа:", result)
        assert result is True

        after = conn.execute(
            "SELECT quantity FROM stock_items WHERE stock_item_id = ?",
            (stock_id,)
        ).fetchone()[0]

        print("Остаток до:", initial)
        print("Остаток после:", after)
        assert after == initial - 1

        invalid = place_order(conn, user_id, -999, size_id, 1)
        print("Несуществующий товар:", invalid)
        assert invalid is False

        order_id = conn.execute(
            "SELECT MAX(order_id) FROM orders"
        ).fetchone()[0]

        result = cancel_order(conn, order_id)
        print("Отмена заказа:", result)
        assert result is True

        restored = conn.execute(
            "SELECT quantity FROM stock_items WHERE stock_item_id = ?",
            (stock_id,)
        ).fetchone()[0]

        print("Остаток после отмены:", restored)
        assert restored == initial

        print("Все проверки пройдены!")

finally:
    conn.close()
