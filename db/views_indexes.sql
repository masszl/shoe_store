
-- 1. Полная информация о заказах
CREATE VIEW IF NOT EXISTS v_orders_full AS
SELECT
    o.order_id,
    o.order_date,
    TRIM(u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '')) AS customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, u.user_id;

-- 2. Товары с остатками
CREATE VIEW IF NOT EXISTS v_products_with_stock AS
SELECT
    p.name AS product_name,
    p.price,
    s.size_value,
    si.quantity AS stock_quantity
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN sizes s ON si.size_id = s.size_id;

-- 3. Статистика по клиентам
CREATE VIEW IF NOT EXISTS v_user_stats AS
SELECT
    TRIM(u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '')) AS customer_name,
    u.login,
    COUNT(o.order_id) AS order_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name, u.middle_name, u.login;

