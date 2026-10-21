--- 1 заказы с данными клиентами
SELECT o.order_id, o.order_date, u.first_name, u.last_name
FROM orders o
INNER JOIN users u ON o.user.id = u.user_id;

--2 товары с моделью и размерами 
SELECT p.product_name,s.size_value
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes s ON si.size_id = s.size_id;

--3 заказы с названиями товаров
SELECT o.order_id,u.first_name,u.last_name,p.product_name
FROM orders o 
INNER JOIN users u ON o.user_id = u.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id;

-- 4 все пользователи и количество их заказов 
SELECT u.user_id, u.first_name,u.last_name,
    COUNT(order_id) AS order_count
FROM users u 
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.first_name, u.last_name;

-- 5. Общее количество пользователей
SELECT COUNT(*) AS total_users
FROM users;

-- 6. Средняя цена товаров
SELECT ROUND(AVG(price), 2) AS average_price
FROM products;

-- 7. Самая низкая и самая высокая цена
SELECT
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products;

-- 8. Общая выручка магазина
SELECT SUM(quantity * price) AS total_revenue
FROM order_items;

---9 КОЛИЧЕСТВО ТОВАРОВ В КАЖДОЙ КАТЕГОРИ
SELECT CATEGORY, COUNT(*) AS total_products
FROM products
GROUP BY manufacturer;

-- 10. Средняя цена товаров каждого производителя
SELECT manufacturer, ROUND(AVG(price), 2) AS average_price
FROM products
GROUP BY manufacturer;

-- 11. Общая сумма покупок каждого клиента
SELECT
    u.user_id,
    u.first_name,
    u.last_name,
    SUM(oi.quantity * oi.price) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.first_name, u.last_name;

-- 12. Количество проданных пар каждой модели
SELECT
    p.product_name,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id
GROUP BY p.product_id, p.product_name;

-- 13. Количество товарных позиций каждого размера
SELECT
    s.size_value,
    COUNT(si.stock_item_id) AS total_items
FROM sizes s
LEFT JOIN stock_items si ON s.size_id = si.size_id
GROUP BY s.size_id, s.size_value;

-- 14. Категории, в которых больше 3 моделей
SELECT category, COUNT(*) AS total_products
FROM products
GROUP BY category
HAVING COUNT(*) > 3;

-- 15. Клиенты, сделавшие больше 2 заказов
SELECT
    u.first_name,
    u.last_name,
    COUNT(o.order_id) AS total_orders
FROM users u
JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(o.order_id) > 2;

-- 16. Модели с выручкой больше 100000 рублей
SELECT
    p.product_name,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.product_id, p.product_name
HAVING SUM(oi.quantity * oi.price) > 100000;


-- 17. Топ-3 самых популярных размеров обуви
SELECT
    s.size_value,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN sizes s ON si.size_id = s.size_id
GROUP BY s.size_id, s.size_value
ORDER BY total_sold DESC
LIMIT 3;

-- 18. Пользователи, которые ничего не заказывали
SELECT
    u.user_id,
    u.first_name,
    u.last_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;

-- 19. Средний чек одного заказа
SELECT ROUND(AVG(order_total), 2) AS average_check
FROM (
    SELECT
        order_id,
        SUM(quantity * price) AS order_total
    FROM order_items
    GROUP BY order_id
);

-- 20. Производитель с наибольшей выручкой
SELECT
    p.manufacturer,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id
GROUP BY p.manufacturer
ORDER BY total_revenue DESC
LIMIT 1;
