
SELECT
    name,
    price,
    calc_discount(price, 20) AS discounted_price
FROM products;

SELECT
    format_full_name(last_name, first_name, middle_name) AS customer_name
FROM users
WHERE middle_name IS NULL OR TRIM(middle_name) = '';

SELECT
    o.order_id,
    pluralize_items(SUM(oi.quantity)) AS total_items
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;

SELECT
    format_full_name(u.last_name, u.first_name, u.middle_name) AS customer_name,
    calc_discount(SUM(oi.quantity * oi.unit_price), 10) AS discounted_total
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, u.user_id;


SELECT
    format_full_name(u.last_name, u.first_name, u.middle_name) AS customer_name,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spent,
    get_client_tier(COALESCE(SUM(oi.quantity * oi.unit_price), 0)) AS client_tier,
    get_client_loyalty_days(MIN(o.order_date)) AS loyalty_days
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.last_name, u.first_name, u.middle_name;
