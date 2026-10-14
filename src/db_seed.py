from db_init import get_connection


def seed_db():
    conn = get_connection()

    try:
        roles = [
            ("Администратор",),
            ("Менеджер",),
            ("Клиент",)
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO roles (role_name) VALUES (?)",
            roles
        )

        sizes = [(36,), (37,), (38,), (39,), (40,)]

        conn.executemany(
            "INSERT OR IGNORE INTO sizes (size_value) VALUES (?)",
            sizes
        )

        role_names = ["Администратор", "Менеджер", "Клиент"]
        role_ids = {}

        for name in role_names:
            role_ids[name] = conn.execute(
                "SELECT role_id FROM roles WHERE role_name = ?",
                (name,)
            ).fetchone()[0]

        users = [
            ("Иванов", "Иван", "Иванович", "admin", role_ids["Администратор"]),
            ("Петров", "Пётр", "Петрович", "manager", role_ids["Менеджер"]),
            ("Сидорова", "Анна", None, "client", role_ids["Клиент"])
        ]

        conn.executemany(
            """INSERT OR IGNORE INTO users
            (last_name, first_name, middle_name, login, role_id)
            VALUES (?, ?, ?, ?, ?)""",
            users
        )

        products = [
            ("Обувь", "Кроссовки", "Nike", "Air Max 90", "images/airmax90.jpg", "Текстиль, кожа", "Повседневные кроссовки", 12990),
            ("Обувь", "Кроссовки", "Adidas", "Superstar", "images/superstar.jpg", "Кожа, резина", "Классические кроссовки", 8990),
            ("Обувь", "Кеды", "Converse", "Chuck Taylor", "images/converse.jpg", "Текстиль, резина", "Высокие кеды", 6990),
            ("Обувь", "Ботинки", "Timberland", "Premium 6", "images/timberland.jpg", "Натуральная кожа", "Демисезонные ботинки", 18990),
            ("Обувь", "Кроссовки", "Puma", "Suede Classic", "images/puma.jpg", "Замша, резина", "Повседневная обувь", 7990)
        ]

        for product in products:
            existing = conn.execute(
                """SELECT product_id FROM products
                WHERE name = ? AND manufacturer = ?""",
                (product[3], product[2])
            ).fetchone()

            if existing is None:
                conn.execute(
                    """INSERT INTO products
                    (category, subcategory, manufacturer, name,
                     image_path, composition, description, price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    product
                )

        stock_data = [
            ("Air Max 90", 38, 10),
            ("Air Max 90", 39, 7),
            ("Superstar", 37, 12),
            ("Superstar", 40, 5),
            ("Chuck Taylor", 36, 8),
            ("Chuck Taylor", 38, 6),
            ("Premium 6", 39, 4),
            ("Premium 6", 40, 3),
            ("Suede Classic", 37, 9),
            ("Suede Classic", 38, 11)
        ]

        for product_name, size_value, quantity in stock_data:
            product = conn.execute(
                """SELECT product_id FROM products
                WHERE name = ?
                ORDER BY product_id LIMIT 1""",
                (product_name,)
            ).fetchone()

            size = conn.execute(
                """SELECT size_id FROM sizes
                WHERE CAST(size_value AS NUMERIC) = ?""",
                (size_value,)
            ).fetchone()

            if product is None:
                raise ValueError(f"Товар не найден: {product_name}")

            if size is None:
                raise ValueError(f"Размер не найден: {size_value}")

            conn.execute(
                """INSERT INTO stock_items
                (product_id, size_id, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(product_id, size_id)
                DO UPDATE SET quantity = excluded.quantity""",
                (product[0], size[0], quantity)
            )

        
        orders_data = [
            ("client", "2026-10-10", [
                ("Air Max 90", 38, 1),
                ("Superstar", 37, 2)
            ]),
            ("manager", "2026-10-11", [
                ("Chuck Taylor", 36, 1),
                ("Premium 6", 39, 1)
            ]),
            ("admin", "2026-10-12", [
                ("Suede Classic", 38, 2),
                ("Air Max 90", 39, 1)
            ])
        ]

        for login, order_date, items in orders_data:
            user = conn.execute(
                "SELECT user_id FROM users WHERE login = ?",
                (login,)
            ).fetchone()

            if user is None:
                raise ValueError(f"Пользователь не найден: {login}")

            existing_order = conn.execute(
                """SELECT order_id FROM orders
                WHERE user_id = ? AND order_date = ?
                ORDER BY order_id LIMIT 1""",
                (user[0], order_date)
            ).fetchone()

            if existing_order:
                order_id = existing_order[0]
            else:
                order_id = conn.execute(
                    """INSERT INTO orders (order_date, user_id)
                    VALUES (?, ?) RETURNING order_id""",
                    (order_date, user[0])
                ).fetchone()[0]

            for product_name, size_value, quantity in items:
                stock = conn.execute(
                    """SELECT s.stock_item_id, p.price
                    FROM stock_items s
                    JOIN products p ON s.product_id = p.product_id
                    JOIN sizes z ON s.size_id = z.size_id
                    WHERE p.name = ?
                    AND CAST(z.size_value AS NUMERIC) = ?""",
                    (product_name, size_value)
                ).fetchone()

                if stock is None:
                    raise ValueError(
                        f"Не найдена позиция: {product_name}, {size_value}"
                    )

                existing_item = conn.execute(
                    """SELECT order_item_id FROM order_items
                    WHERE order_id = ? AND stock_item_id = ?""",
                    (order_id, stock[0])
                ).fetchone()

                if existing_item is None:
                    conn.execute(
                        """INSERT INTO order_items
                        (order_id, stock_item_id, quantity, unit_price)
                        VALUES (?, ?, ?, ?)""",
                        (order_id, stock[0], quantity, stock[1])
                    )


        conn.commit()

        for table in ["roles", "users", "products", "sizes", "stock_items"]:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table}: {count}")

        print("Данные успешно добавлены!")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    seed_db()
