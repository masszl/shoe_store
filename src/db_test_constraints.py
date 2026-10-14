
from db_init import get_connection
import sqlite3

conn = get_connection()

def test_constraint(name, sql, params):
    conn.execute("SAVEPOINT test_case")

    try:
        conn.execute(sql, params)
        print(f"[FAIL] {name}: ошибка не возникла")
    except sqlite3.IntegrityError:
        print(f"[PASS] {name}: ограничение сработало")
    finally:
        conn.execute("ROLLBACK TO SAVEPOINT test_case")
        conn.execute("RELEASE SAVEPOINT test_case")

test_constraint(
    "NOT NULL: фамилия",
    "INSERT INTO users (last_name, first_name, login, role_id) VALUES (?, ?, ?, ?)",
    (None, "Иван", "test_user", 1)
)

test_constraint(
    "CHECK: отрицательная цена",
    """INSERT INTO products
    (category, subcategory, manufacturer, name, image_path, price)
    VALUES (?, ?, ?, ?, ?, ?)""",
    ("Обувь", "Кроссовки", "Nike", "Test", "test.png", -100)
)

test_constraint(
    "CHECK: отрицательный остаток",
    "INSERT INTO stock_items (product_id, size_id, quantity) VALUES (?, ?, ?)",
    (1, 1, -5)
)

test_constraint(
    "FOREIGN KEY: несуществующая роль",
    """INSERT INTO users
    (last_name, first_name, login, role_id)
    VALUES (?, ?, ?, ?)""",
    ("Иванов", "Иван", "invalid_role", 999999)
)



conn.execute("SAVEPOINT unique_test")

try:
    conn.execute(
        """INSERT INTO roles (role_name)
        VALUES (?)""",
        ("Тестовая роль",)
    )

    role_id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    conn.execute(
        """INSERT INTO users
        (last_name, first_name, login, role_id)
        VALUES (?, ?, ?, ?)""",
        ("Иванов", "Иван", "test_unique", role_id)
    )

    try:
        conn.execute(
            """INSERT INTO users
            (last_name, first_name, login, role_id)
            VALUES (?, ?, ?, ?)""",
            ("Петров", "Пётр", "test_unique", role_id)
        )
        print("[FAIL] UNIQUE: повторяющийся логин разрешён")
    except sqlite3.IntegrityError:
        print("[PASS] UNIQUE: повторяющийся логин запрещён")

finally:
    conn.execute("ROLLBACK TO SAVEPOINT unique_test")
    conn.execute("RELEASE SAVEPOINT unique_test")


conn.execute("SAVEPOINT delete_test")

try:
    role_id = conn.execute(
        "INSERT INTO roles (role_name) VALUES (?) RETURNING role_id",
        ("Роль для проверки удаления",)
    ).fetchone()[0]

    user_id = conn.execute(
        """INSERT INTO users
        (last_name, first_name, login, role_id)
        VALUES (?, ?, ?, ?) RETURNING user_id""",
        ("Тестов", "Иван", "delete_test_user", role_id)
    ).fetchone()[0]

    try:
        conn.execute(
            "DELETE FROM roles WHERE role_id = ?",
            (role_id,)
        )
        print("[FAIL] RESTRICT: роль удалена")
    except sqlite3.IntegrityError:
        print("[PASS] RESTRICT: удаление роли запрещено")

    product_id = conn.execute(
        """INSERT INTO products
        (category, subcategory, manufacturer, name, image_path, price)
        VALUES (?, ?, ?, ?, ?, ?) RETURNING product_id""",
        ("Обувь", "Кроссовки", "Test", "Test", "test.png", 1000)
    ).fetchone()[0]

    size_id = conn.execute(
        "INSERT INTO sizes (size_value) VALUES (?) RETURNING size_id",
        (99,)
    ).fetchone()[0]

    stock_id = conn.execute(
        """INSERT INTO stock_items (product_id, size_id, quantity)
        VALUES (?, ?, ?) RETURNING stock_item_id""",
        (product_id, size_id, 10)
    ).fetchone()[0]

    order_id = conn.execute(
        "INSERT INTO orders (user_id) VALUES (?) RETURNING order_id",
        (user_id,)
    ).fetchone()[0]

    conn.execute(
        """INSERT INTO order_items
        (order_id, stock_item_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)""",
        (order_id, stock_id, 2, 1000)
    )

    conn.execute(
        "DELETE FROM orders WHERE order_id = ?",
        (order_id,)
    )

    count = conn.execute(
        "SELECT COUNT(*) FROM order_items WHERE order_id = ?",
        (order_id,)
    ).fetchone()[0]

    if count == 0:
        print("[PASS] CASCADE: позиции заказа удалены")
    else:
        print("[FAIL] CASCADE: позиции заказа остались")

finally:
    conn.execute("ROLLBACK TO SAVEPOINT delete_test")
    conn.execute("RELEASE SAVEPOINT delete_test")


conn.close()
