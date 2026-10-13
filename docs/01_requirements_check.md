# Проверка требований «Чудо Обувь»

## 1. Проверка функциональных требований

| Требование | Таблица | Поле | Операция |
|---|---|---|---|
| Просмотр каталога | products | name, price | SELECT |
| Количество доступной обуви | stock_items | quantity | SELECT |
| Изображение модели | products | image_path | SELECT |
| Выбор модели и размера | stock_items | product_id, size_id | SELECT |
| Оформление заказа | orders | user_id, order_date | INSERT |
| Добавление товаров в заказ | order_items | stock_item_id, quantity | INSERT |
| Изменение количества | order_items | quantity | UPDATE |
| Удаление позиции заказа | order_items | order_item_id | DELETE |
| Просмотр списка заказов | orders, users | order_date, last_name, first_name, middle_name | SELECT |
| Управление заказами | orders, order_items | order_id | INSERT, UPDATE, DELETE |
| Поиск товаров | products | name, manufacturer | SELECT |
| Фильтрация товаров | products | category, subcategory | SELECT |
| Сортировка товаров | products | price, name | SELECT |

## 2. Проверка ролей пользователей

### Неавторизованный пользователь
Может просматривать каталог товаров.
Используется таблица products.
Операция: SELECT.

### Авторизованный пользователь
Может просматривать каталог, искать товары,
оформлять заказы и изменять их состав.
Используются products, stock_items, orders,
order_items.
Операции: SELECT, INSERT, UPDATE, DELETE.

### Менеджер
Может просматривать каталог и заказы,
создавать и удалять заказы.
Используются products, orders, order_items.
Операции: SELECT, INSERT, DELETE.

### Администратор
Имеет права менеджера и может редактировать
заказы.
Используются все необходимые таблицы.
Операции: SELECT, INSERT, UPDATE, DELETE.

## 3. Авторизация

Таблица: users.
Поле: login.

Вход выполняется по логину без пароля.
Логин должен быть уникальным.

Роль определяется через users.role_id
и таблицу roles.

## 4. Проверка структуры

В базе данных предусмотрено семь таблиц:
roles, users, products, sizes, stock_items,
orders, order_items.

Каждая таблица имеет первичный ключ.
Связи реализованы через внешние ключи.

## Вывод

Разработанная структура базы данных позволяет
реализовать основные требования системы
«Чудо Обувь».

Права пользователей должны дополнительно
проверяться при разработке приложения.
