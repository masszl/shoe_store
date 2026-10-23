-- 1. Товары дороже средней цены
SELECT product_name, price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
);

-- 2. Клиент с самым дорогим заказом
SELECT
    u.first_name,
    u.last_name,
    SUM(oi.quantity * oi.price) AS total_price
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, u.user_id, u.first_name, u.last_name
HAVING SUM(oi.quantity * oi.price) = (
    SELECT MAX(order_total)
    FROM (
        SELECT SUM(quantity * price) AS order_total
        FROM order_items
        GROUP BY order_id
    )
);


-- 3. Клиенты, у которых есть хотя бы один заказ
SELECT last_name
FROM users
WHERE user_id IN (
    SELECT user_id
    FROM orders
);

-- 4. Пользователи, которые ничего не заказывали
SELECT user_id, first_name, last_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.user_id
);

-- 5. Товары, которые ни разу не заказывали
SELECT product_name
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM stock_items si
    JOIN order_items oi
        ON si.stock_item_id = oi.stock_item_id
    WHERE si.product_id = p.product_id
);



-- 6. Рейтинг клиентов по общей сумме покупок
SELECT
    u.first_name,
    u.last_name,
    COALESCE(SUM(oi.quantity * oi.price), 0) AS total_spent,
    RANK() OVER (
        ORDER BY COALESCE(SUM(oi.quantity * oi.price), 0) DESC
    ) AS client_rank
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.first_name, u.last_name
ORDER BY client_rank;

-- 7. Нумерация заказов каждого клиента
SELECT
    o.order_id,
    u.first_name,
    u.last_name,
    o.order_date,
    ROW_NUMBER() OVER (
        PARTITION BY o.user_id
        ORDER BY o.order_date, o.order_id
    ) AS order_number
FROM orders o
JOIN users u ON o.user_id = u.user_id;

-- 8. Нумерация товаров по цене внутри категорий
SELECT
    product_name,
    category,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY category
        ORDER BY price DESC, product_id
    ) AS product_number
FROM products;

-- 9. Самый дорогой товар в каждой категории
SELECT
    category,
    product_name,
    price
FROM (
    SELECT
        category,
        product_name,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY price DESC, product_id
        ) AS rn
    FROM products
)
WHERE rn = 1;


-- 10. Накопительная сумма заказов по датам
SELECT
    o.order_id,
    o.order_date,
    SUM(oi.quantity * oi.price) AS order_total,
    SUM(SUM(oi.quantity * oi.price)) OVER (
        ORDER BY o.order_date, o.order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date
ORDER BY o.order_date, o.order_id;

-- 11. Дата предыдущего заказа и разница в днях
SELECT
    order_id,
    user_id,
    order_date,
    previous_date,
    ROUND(
        julianday(order_date) - julianday(previous_date),
        0
    ) AS days_difference
FROM (
    SELECT
        order_id,
        user_id,
        order_date,
        LAG(order_date) OVER (
            PARTITION BY user_id
            ORDER BY order_date, order_id
        ) AS previous_date
    FROM orders
)
ORDER BY user_id, order_date, order_id;
