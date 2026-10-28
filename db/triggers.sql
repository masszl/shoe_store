CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT,
    operation TEXT,
    record_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    changed_at TEXT DEFAULT (datetime('now'))
);

CREATE TRIGGER IF NOT EXISTS trg_products_price_update
AFTER UPDATE OF price ON products
FOR EACH ROW
WHEN OLD.price IS NOT NEW.price
BEGIN
    INSERT INTO audit_log (
        table_name, operation, record_id,
        old_value, new_value
    )
    VALUES (
        'products', 'UPDATE', NEW.product_id,
        CAST(OLD.price AS TEXT),
        CAST(NEW.price AS TEXT)
    );
END;

CREATE TRIGGER IF NOT EXISTS trg_orders_delete
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        table_name, operation, record_id,
        old_value, new_value
    )
    VALUES (
        'orders', 'DELETE', OLD.order_id,
        CAST(OLD.order_id AS TEXT), NULL
    );
END;

CREATE TRIGGER IF NOT EXISTS trg_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
WHEN NEW.updated_at IS OLD.updated_at
BEGIN
    UPDATE users
    SET updated_at = datetime('now')
    WHERE user_id = NEW.user_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_order_items_stock
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.quantity <= 0 THEN
            RAISE(ABORT, 'Количество должно быть положительным')
        WHEN NOT EXISTS (
            SELECT 1
            FROM stock_items
            WHERE stock_item_id = NEW.stock_item_id
              AND quantity >= NEW.quantity
        ) THEN
            RAISE(ABORT, 'Недостаточно товара на складе')
    END;

    UPDATE stock_items
    SET quantity = quantity - NEW.quantity
    WHERE stock_item_id = NEW.stock_item_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_users_delete_protect
BEFORE DELETE ON users
FOR EACH ROW
WHEN EXISTS (
    SELECT 1
    FROM orders
    WHERE user_id = OLD.user_id
)
BEGIN
    SELECT RAISE(
        ABORT,
        'Нельзя удалить пользователя с активными заказами'
    );
END;

CREATE TRIGGER IF NOT EXISTS trg_stock_items_insert_check
BEFORE INSERT ON stock_items
FOR EACH ROW
WHEN NEW.quantity < 0
BEGIN
    SELECT RAISE(
        ABORT,
        'Количество не может быть отрицательным'
    );
END;
