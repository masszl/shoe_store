# Ограничения базы данных «Чудо Обувь»

## Таблица roles

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| role_id | Да | Да (PK) | - | - |
| role_name | Да | Да | - | - |

## Таблица users

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| user_id | Да | Да (PK) | - | - |
| last_name | Да | Нет | - | - |
| first_name | Да | Нет | - | - |
| middle_name | Нет | Нет | - | NULL |
| login | Да | Да | - | - |
| role_id | Да | Нет | - | - |

## Таблица products

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| product_id | Да | Да (PK) | - | - |
| category | Да | Нет | - | - |
| subcategory | Да | Нет | - | - |
| manufacturer | Да | Нет | - | - |
| name | Да | Нет | - | - |
| image_path | Да | Нет | - | - |
| composition | Нет | Нет | - | NULL |
| description | Нет | Нет | - | NULL |
| price | Да | Нет | price > 0 | - |

## Таблица sizes

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| size_id | Да | Да (PK) | - | - |
| size_value | Да | Да | - | - |

## Таблица stock_items

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| stock_item_id | Да | Да (PK) | - | - |
| product_id | Да | Составной UNIQUE | - | - |
| size_id | Да | Составной UNIQUE | - | - |
| quantity | Да | Нет | quantity >= 0 | 0 |

Дополнительное ограничение:
UNIQUE (product_id, size_id).

## Таблица orders

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| order_id | Да | Да (PK) | - | - |
| order_date | Да | Нет | - | CURRENT_DATE |
| user_id | Да | Нет | - | - |

## Таблица order_items

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| order_item_id | Да | Да (PK) | - | - |
| order_id | Да | Нет | - | - |
| stock_item_id | Да | Нет | - | - |
| quantity | Да | Нет | quantity > 0 | - |
| unit_price | Да | Нет | unit_price > 0 | - |

## Внешние ключи и правила удаления

- users.role_id → roles.role_id — ON DELETE RESTRICT
- orders.user_id → users.user_id — ON DELETE RESTRICT
- stock_items.product_id → products.product_id — ON DELETE RESTRICT
- stock_items.size_id → sizes.size_id — ON DELETE RESTRICT
- order_items.order_id → orders.order_id — ON DELETE CASCADE
- order_items.stock_item_id → stock_items.stock_item_id — ON DELETE RESTRICT



# Отчёт о проверке ограничений базы данных

## Цель работы

Проверить правильность работы ограничений базы данных shoe_store.

## Проверяемые ограничения

| № | Ограничение | Проверка | Ожидаемый результат |
|---|---|---|---|
| 1 | NOT NULL | Пользователь без фамилии | Ошибка |
| 2 | CHECK | Отрицательная цена товара | Ошибка |
| 3 | CHECK | Отрицательный остаток | Ошибка |
| 4 | FOREIGN KEY | Несуществующая роль | Ошибка |
| 5 | UNIQUE | Одинаковые логины | Ошибка |
| 6 | ON DELETE RESTRICT | Удаление используемой роли | Ошибка |
| 7 | ON DELETE CASCADE | Удаление заказа | Удаляются позиции заказа |

## Выполнение проверки

Для тестирования создан файл src/db_test_constraints.py.

Тесты выполняются командой:

py src/db_test_constraints.py

После каждого тестирования временные данные откатываются.

## Результаты

| Ограничение | Результат |
|---|---|
| NOT NULL | Не проверено |
| CHECK: цена | Не проверено |
| CHECK: остаток | Не проверено |
| FOREIGN KEY | Не проверено |
| UNIQUE | Не проверено |
| ON DELETE RESTRICT | Не проверено |
| ON DELETE CASCADE | Не проверено |

## Вывод

Подготовлены тесты основных ограничений базы данных.

После успешного запуска необходимо заменить
«Не проверено» на «PASS» и указать фактические результаты.
