
SELECT
    p.name AS product_name,
    s.size_value AS size,
    st.quantity AS stock_quantity,
    p.price
FROM stock_items st
JOIN products p ON st.product_id = p.product_id
JOIN sizes s ON st.size_id = s.size_id
ORDER BY p.name, s.size_value;


SELECT
    o.order_id,
    o.order_date,
    u.login,
    p.name AS product_name,
    s.size_value AS size,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS total
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stock_items st ON oi.stock_item_id = st.stock_item_id
JOIN products p ON st.product_id = p.product_id
JOIN sizes s ON st.size_id = s.size_id
ORDER BY o.order_id;


SELECT
    o.order_id,
    u.login,
    SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, u.login
ORDER BY o.order_id;
