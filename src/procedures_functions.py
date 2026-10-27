
import sqlite3
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "database.db"
TEST_DB_PATH = ROOT / "db" / "database_procedures_test.db"


def calc_order_total(price, quantity):
    try:
        price = Decimal(str(price))
        quantity = int(quantity)
        if quantity <= 0:
            return 0
        return round(float(price * quantity), 2)
    except (ValueError, TypeError, InvalidOperation):
        return 0


def get_category_count(conn, category_name):
    if category_name is None:
        return 0
    row = conn.execute(
        "SELECT COUNT(*) FROM products WHERE category = ?",
        (category_name,)
    ).fetchone()
    return row[0]


def format_phone(phone):
    if phone is None:
        return None

    phone = str(phone).strip()

    if len(phone) == 11 and phone.isdigit() and phone[0] in "78":
        return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"

    return phone


def create_order(conn, user_id, stock_item_id, quantity):
    if not isinstance(quantity, int) or quantity <= 0:
        return False

    try:
        conn.execute("BEGIN")

        user = conn.execute(
            "SELECT user_id FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        stock = conn.execute("""
            SELECT si.quantity, p.price
            FROM stock_items si
            JOIN products p ON p.product_id = si.product_id
            WHERE si.stock_item_id = ?
        """, (stock_item_id,)).fetchone()

        if not user or not stock or stock[0] < quantity:
            conn.rollback()
            return False

        cursor = conn.execute(
            "INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
            (datetime.now().strftime("%Y-%m-%d"), user_id)
        )

        conn.execute("""
            INSERT INTO order_items
            (order_id, stock_item_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (cursor.lastrowid, stock_item_id, quantity, stock[1]))

        update_stock(conn, stock_item_id, quantity, commit=False)

        conn.commit()
        return True

    except (sqlite3.Error, ValueError) as error:
        conn.rollback()
        print("Ошибка создания заказа:", error)
        return False


def update_stock(conn, stock_item_id, quantity_sold, commit=True):
    if not isinstance(quantity_sold, int) or quantity_sold <= 0:
        conn.rollback()
        raise ValueError("Количество должно быть положительным")

    try:
        cursor = conn.execute("""
            UPDATE stock_items
            SET quantity = quantity - ?
            WHERE stock_item_id = ? AND quantity >= ?
        """, (quantity_sold, stock_item_id, quantity_sold))

        if cursor.rowcount != 1:
            raise ValueError("Недостаточно товара на складе")

        if commit:
            conn.commit()

        return True

    except (sqlite3.Error, ValueError):
        conn.rollback()
        raise


def get_sales_report(conn, start_date, end_date):
    total = conn.execute("""
        SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
    """, (start_date, end_date)).fetchone()[0]

    return (
        f"С {start_date} по {end_date} продано товаров "
        f"на сумму {total:.2f} руб."
    )


def register_functions(conn, count_conn):
    conn.create_function("calculate_total", 2, calc_order_total)
    conn.create_function("format_phone", 1, format_phone)
    conn.create_function(
        "count_in_category",
        1,
        lambda category: get_category_count(count_conn, category)
    )


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"База не найдена: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as source:
        with sqlite3.connect(TEST_DB_PATH) as backup:
            source.backup(backup)

    conn = sqlite3.connect(TEST_DB_PATH)
    count_conn = sqlite3.connect(TEST_DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        register_functions(conn, count_conn)

        print("1. Суммы заказов")
        rows = conn.execute("""
            SELECT order_id,
                   SUM(calculate_total(unit_price, quantity))
            FROM order_items
            GROUP BY order_id
        """).fetchall()
        for row in rows:
            print(row)

        print("\n2. Количество товаров по категориям")
        rows = conn.execute("""
            SELECT DISTINCT category,
                   count_in_category(category)
            FROM products
        """).fetchall()
        for row in rows:
            print(row)

        print("\n3. Форматирование телефона")
        print(conn.execute(
            "SELECT format_phone('89991234567')"
        ).fetchone()[0])

        print("\n4. Создание заказа")
        data = conn.execute("""
            SELECT u.user_id, si.stock_item_id, si.quantity
            FROM users u
            CROSS JOIN stock_items si
            WHERE si.quantity > 0
            LIMIT 1
        """).fetchone()

        if data:
            user_id, stock_id, initial_stock = data

            result = create_order(conn, user_id, stock_id, 1)
            print("Заказ создан:", result)

            current_stock = conn.execute(
                "SELECT quantity FROM stock_items WHERE stock_item_id = ?",
                (stock_id,)
            ).fetchone()[0]

            print("Остаток до:", initial_stock)
            print("Остаток после:", current_stock)

            assert result is True
            assert current_stock == initial_stock - 1

            print("\n5. Проверка ошибки при списании")
            try:
                update_stock(conn, stock_id, 999999)
            except ValueError as error:
                print(error)

            checked_stock = conn.execute(
                "SELECT quantity FROM stock_items WHERE stock_item_id = ?",
                (stock_id,)
            ).fetchone()[0]

            assert checked_stock == current_stock
            print("Откат проверен")
        else:
            print("Нет доступного товара или пользователя")

        print("\n6. Отчёт по продажам")
        print(get_sales_report(conn, "2020-01-01", "2030-12-31"))

        print("\nВсе проверки завершены")

    finally:
        count_conn.close()
        conn.close()


if __name__ == "__main__":
    main()
