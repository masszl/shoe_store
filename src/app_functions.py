import sqlite3
from datetime import datetime

def calc_discount(price, discount_percent):
    if price is None or discount_percent is None:
        return 0.0

    discount_percent = max(0, min(100, discount_percent))
    return round(price * (1 - discount_percent / 100), 2)


def pluralize_items(count):
    if count is None:
        return "0 товаров"

    count = int(count)

    if count % 100 in (11, 12, 13, 14):
        word = "товаров"
    elif count % 10 == 1:
        word = "товар"
    elif count % 10 in (2, 3, 4):
        word = "товара"
    else:
        word = "товаров"

    return f"{count} {word}"


def format_full_name(last, first, middle):
    if not last or not first:
        return "Аноним"

    last = last.strip().capitalize()
    first = first.strip().capitalize()
    middle = middle.strip().capitalize() if middle else ""

    if not last or not first:
        return "Аноним"

    result = f"{last} {first[0]}."

    if middle:
        result += f"{middle[0]}."

    return result


def place_order(conn, user_id, product_id, size_id, quantity):
    if not isinstance(quantity, int) or quantity <= 0:
        return False

    try:
        with conn:
            user = conn.execute(
                "SELECT user_id FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()

            if not user:
                return False

            stock = conn.execute("""
                SELECT si.stock_item_id, si.quantity, p.price
                FROM stock_items si
                JOIN products p ON si.product_id = p.product_id
                WHERE si.product_id = ? AND si.size_id = ?
            """, (product_id, size_id)).fetchone()

            if not stock:
                return False

            stock_id, available, price = stock

            if available < quantity:
                print("Недостаточно товара на складе")
                return False

            cursor = conn.execute(
                "INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
                (datetime.now().strftime("%Y-%m-%d"), user_id)
            )

            order_id = cursor.lastrowid

            conn.execute("""
                INSERT INTO order_items
                (order_id, stock_item_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """, (order_id, stock_id, quantity, price))

            conn.execute("""
                UPDATE stock_items
                SET quantity = quantity - ?
                WHERE stock_item_id = ?
            """, (quantity, stock_id))

        return True

    except sqlite3.Error as error:
        conn.rollback()
        print("Ошибка:", error)
        return False


def get_client_tier(total_spent):
    if total_spent is None:
        return "Без статуса"

    try:
        total_spent = float(total_spent)
    except (ValueError, TypeError):
        return "Без статуса"

    if total_spent < 0:
        return "Без статуса"
    if total_spent < 5000:
        return "Новичок"
    if total_spent < 20000:
        return "Бронза"
    if total_spent < 50000:
        return "Серебро"
    if total_spent <= 100000:
        return "Золото"

    return "Платина"


def get_client_loyalty_days(first_order_date_str):
    if not first_order_date_str:
        return 0

    try:
        first_date = datetime.strptime(
            first_order_date_str[:10], "%Y-%m-%d"
        )
        return max(0, (datetime.now() - first_date).days)
    except (ValueError, TypeError):
        return 0

