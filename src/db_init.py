import sqlite3  
from pathlib import Path 

DB_path = Path(__file__).parent.parent / "db" / "database.db"

def get_connection():
    DB_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn 

def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
        )
        """)

    conn.execute("""
            CREATE TABLE IF NOT EXISTS sizes (
            size_id INTEGER PRIMARY KEY AUTOINCREMENT,
            size_value TEXT NOT NULL UNIQUE
            )
            """)

    conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                manufacter TEXT NOT NULL,
                name TEXT NOT NULL,
                image_path TEXT NOT NULL,
                composition  TEXT,
                descripton TEXT,
                price NUMERIC NOT NULL CHECK (price > 0)
                )
                """)

    conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    login TEXT NOT NULL UNIQUE,
                    role_id INTEGER NOT NULL,
                    FOREIGN KEY(role_id) REFERENCES roles(role_id)
                        ON DELETE RESTRICT
                    )
                    """)

    conn.execute("""
            CREATE TABLE IF NOT EXISTS stock_items (
            stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            size_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
            UNIQUE (product_id, size_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
                ON DELETE RESTRICT,
            FOREIGN KEY (size_id) REFERENCES sizes(size_id)
                ON DELETE RESTRICT
        )
    """)

    conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE RESTRICT
            )
        """)


    conn.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            stock_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price NUMERIC NOT NULL CHECK (unit_price > 0),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
                ON DELETE CASCADE,
            FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id)
                ON DELETE RESTRICT
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()   
    print("База данных создана ")