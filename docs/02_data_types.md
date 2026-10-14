# Типы данных базы «Чудо Обувь»

## Таблица roles
- role_id (PK) — идентификатор роли
- role_name — название роли

## Таблица users
- user_id (PK) — идентификатор пользователя
- last_name — фамилия
- first_name — имя
- middle_name — отчество
- login — логин
- role_id (FK) — ссылка на роль

## Таблица products
- product_id (PK) — идентификатор товара
- category — категория
- subcategory — подкатегория
- manufacturer — производитель
- name — название товара
- image_path — путь к изображению
- composition — состав
- description — описание
- price — цена

## Таблица sizes
- size_id (PK) — идентификатор размера
- size_value — значение размера

## Таблица stock_items
- stock_item_id (PK) — идентификатор позиции
- product_id (FK) — ссылка на товар
- size_id (FK) — ссылка на размер
- quantity — количество на складе

## Таблица orders
- order_id (PK) — идентификатор заказа
- order_date — дата заказа
- user_id (FK) — ссылка на пользователя

## Таблица order_items
- order_item_id (PK) — идентификатор позиции заказа
- order_id (FK) — ссылка на заказ
- stock_item_id (FK) — ссылка на товарную позицию
- quantity — количество
- unit_price — цена за единицу



## Типы данных SQLite

### Таблица users

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| user_id | INTEGER | Идентификатор пользователя | Да | - | PRIMARY KEY AUTOINCREMENT |
| last_name | TEXT | Фамилия | Да | - | - |
| first_name | TEXT | Имя | Да | - | - |
| middle_name | TEXT | Отчество | Нет | NULL | - |
| login | TEXT | Логин | Да | - | UNIQUE |
| role_id | INTEGER | Ссылка на роль | Да | - | FOREIGN KEY |



### Таблица roles

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| role_id | INTEGER | Идентификатор роли | Да | - | PRIMARY KEY AUTOINCREMENT |
| role_name | TEXT | Название роли | Да | - | UNIQUE |

### Таблица products

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| product_id | INTEGER | Идентификатор товара | Да | - | PRIMARY KEY AUTOINCREMENT |
| category | TEXT | Категория | Да | - | - |
| subcategory | TEXT | Подкатегория | Да | - | - |
| manufacturer | TEXT | Производитель | Да | - | - |
| name | TEXT | Наименование | Да | - | - |
| image_path | TEXT | Путь к изображению | Да | - | - |
| composition | TEXT | Состав | Нет | NULL | - |
| description | TEXT | Описание | Нет | NULL | - |
| price | NUMERIC | Цена товара | Да | - | CHECK (price > 0) |

### Таблица sizes

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| size_id | INTEGER | Идентификатор размера | Да | - | PRIMARY KEY AUTOINCREMENT |
| size_value | NUMERIC | Размер обуви | Да | - | UNIQUE |

### Таблица stock_items

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| stock_item_id | INTEGER | Идентификатор позиции | Да | - | PRIMARY KEY AUTOINCREMENT |
| product_id | INTEGER | Ссылка на товар | Да | - | FOREIGN KEY |
| size_id | INTEGER | Ссылка на размер | Да | - | FOREIGN KEY |
| quantity | INTEGER | Остаток на складе | Да | 0 | CHECK (quantity >= 0) |

Дополнительное ограничение: UNIQUE (product_id, size_id).

### Таблица orders

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| order_id | INTEGER | Идентификатор заказа | Да | - | PRIMARY KEY AUTOINCREMENT |
| order_date | TEXT | Дата заказа | Да | CURRENT_DATE | ISO 8601 |
| user_id | INTEGER | Ссылка на пользователя | Да | - | FOREIGN KEY |

### Таблица order_items

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| order_item_id | INTEGER | Идентификатор позиции заказа | Да | - | PRIMARY KEY AUTOINCREMENT |
| order_id | INTEGER | Ссылка на заказ | Да | - | FOREIGN KEY |
| stock_item_id | INTEGER | Ссылка на товарную позицию | Да | - | FOREIGN KEY |
| quantity | INTEGER | Количество товара | Да | - | CHECK (quantity > 0) |
| unit_price | NUMERIC | Цена на момент заказа | Да | - | CHECK (unit_price > 0) |
