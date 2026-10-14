import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "db" / "database_day3_test.db"


def test_constraint(conn, name, query, params):
    try:
        conn.execute(query, params)
        print(f"[FAIL] {name}: неправильные данные приняты")
        conn.rollback()
    except sqlite3.IntegrityError:
        print(f"[PASS] {name}: неправильные данные отклонены")
        conn.rollback()


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        test_constraint(
            conn,
            "Пустое название товара",
            """
            INSERT INTO products
            (category, subcategory, manufacturer, name, image_path, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Обувь", "Кроссовки", "Nike", "", "nike.jpg", 5000)
        )

        test_constraint(
            conn,
            "Отрицательная цена",
            """
            INSERT INTO products
            (category, subcategory, manufacturer, name, image_path, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Обувь", "Кроссовки", "Nike", "Air Max", "nike.jpg", -100)
        )

        test_constraint(
            conn,
            "Слишком высокая цена",
            """
            INSERT INTO products
            (category, subcategory, manufacturer, name, image_path, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Обувь", "Кроссовки", "Nike", "Air Max", "nike.jpg", 1500000)
        )

        test_constraint(
            conn,
            "Короткий логин",
            """
            INSERT INTO users
            (last_name, first_name, login, role_id)
            VALUES (?, ?, ?, ?)
            """,
            ("Иванов", "Иван", "ab", 1)
        )

        test_constraint(
            conn,
            "Недопустимый размер обуви",
            "INSERT INTO sizes (size_value) VALUES (?)",
            (55,)
        )

        test_constraint(
            conn,
            "Отрицательный остаток",
            """
            INSERT INTO stock_items
            (product_id, size_id, quantity)
            VALUES (?, ?, ?)
            """,
            (1, 1, -5)
        )

        test_constraint(
            conn,
            "Нулевое количество в заказе",
            """
            INSERT INTO order_items
            (order_id, stock_item_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
            """,
            (1, 1, 0, 5000)
        )

        test_constraint(
            conn,
            "Нулевая цена позиции заказа",
            """
            INSERT INTO order_items
            (order_id, stock_item_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
            """,
            (1, 1, 1, 0)
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
