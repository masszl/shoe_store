import sqlite3
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parent.parent
source_path = root / "db" / "database.db"
test_path = root / "db" / "database_triggers_test.db"

with sqlite3.connect(source_path) as source:
    with sqlite3.connect(test_path) as backup:
        source.backup(backup)

conn = sqlite3.connect(test_path)
conn.execute("PRAGMA foreign_keys = ON")

try:
    triggers = conn.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'trigger'
    """).fetchall()

    print("Количество триггеров:", len(triggers))
    assert len(triggers) >= 6

    user_id = conn.execute(
        "SELECT user_id FROM users LIMIT 1"
    ).fetchone()[0]

    stock = conn.execute("""
        SELECT si.stock_item_id, si.quantity, p.price
        FROM stock_items si
        JOIN products p ON p.product_id = si.product_id
        WHERE si.quantity > 0
        LIMIT 1
    """).fetchone()

    stock_id, before, price = stock

    cursor = conn.execute("""
        INSERT INTO orders (order_date, user_id)
        VALUES (?, ?)
    """, (datetime.now().strftime("%Y-%m-%d"), user_id))

    order_id = cursor.lastrowid

    conn.execute("""
        INSERT INTO order_items
        (order_id, stock_item_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, (order_id, stock_id, 1, price))

    after = conn.execute("""
        SELECT quantity FROM stock_items
        WHERE stock_item_id = ?
    """, (stock_id,)).fetchone()[0]

    print("Остаток до:", before)
    print("Остаток после:", after)

    assert after == before - 1
    print("Списание товара: успешно")

    try:
        conn.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,)
        )
        raise AssertionError("Удаление не было заблокировано")
    except sqlite3.IntegrityError as error:
        print("Защита пользователя:", error)

    product = conn.execute(
        "SELECT product_id, price FROM products LIMIT 1"
    ).fetchone()

    product_id, old_price = product

    conn.execute("""
        UPDATE products SET price = ?
        WHERE product_id = ?
    """, (old_price + 100, product_id))

    log = conn.execute("""
        SELECT operation, old_value, new_value
        FROM audit_log
        WHERE table_name = 'products'
          AND record_id = ?
        ORDER BY log_id DESC
        LIMIT 1
    """, (product_id,)).fetchone()

    assert log is not None
    print("Аудит изменения цены:", log)

    conn.execute(
        "DELETE FROM order_items WHERE order_id = ?",
        (order_id,)
    )
    conn.execute(
        "DELETE FROM orders WHERE order_id = ?",
        (order_id,)
    )

    deleted_log = conn.execute("""
        SELECT operation FROM audit_log
        WHERE table_name = 'orders'
          AND record_id = ?
        ORDER BY log_id DESC
        LIMIT 1
    """, (order_id,)).fetchone()

    assert deleted_log == ("DELETE",)
    print("Аудит удаления заказа: успешно")

    print("\nПервые 5 записей журнала:")
    for row in conn.execute("""
        SELECT * FROM audit_log
        ORDER BY log_id
        LIMIT 5
    """):
        print(row)

    print("\nВсе проверки пройдены!")

finally:
    conn.rollback()
    conn.close()
