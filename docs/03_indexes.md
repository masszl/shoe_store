# Индексы базы данных

Для ускорения поиска и соединения таблиц добавлены индексы.

| Индекс | Таблица | Поле |
|---|---|---|
| idx_users_role_id | users | role_id |
| idx_orders_user_id | orders | user_id |
| idx_stock_items_product_id | stock_items | product_id |
| idx_stock_items_size_id | stock_items | size_id |
| idx_order_items_order_id | order_items | order_id |
| idx_order_items_stock_item_id | order_items | stock_item_id |
| idx_products_category | products | category |
| idx_products_manufacturer | products | manufacturer |
| idx_orders_order_date | orders | order_date |

Всего предусмотрено 9 индексов. Они используются для поиска связанных записей и фильтрации товаров и заказов.
