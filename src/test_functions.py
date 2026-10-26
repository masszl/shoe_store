from app_functions import (
    calc_discount,
    pluralize_items,
    format_full_name,
    get_client_tier,
    get_client_loyalty_days
)

assert calc_discount(1000, 20) == 800.0
assert calc_discount(1000, 0) == 1000.0
assert calc_discount(1000, 100) == 0.0
assert calc_discount(1000, -10) == 1000.0
assert calc_discount(1000, 150) == 0.0
assert calc_discount(None, 20) == 0.0

assert pluralize_items(1) == "1 товар"
assert pluralize_items(2) == "2 товара"
assert pluralize_items(5) == "5 товаров"
assert pluralize_items(11) == "11 товаров"
assert pluralize_items(21) == "21 товар"
assert pluralize_items(None) == "0 товаров"

assert format_full_name("иванов", "иван", "иванович") == "Иванов И.И."
assert format_full_name("петров", "петр", None) == "Петров П."
assert format_full_name(None, "Иван", None) == "Аноним"
assert format_full_name("", "Иван", None) == "Аноним"

assert get_client_tier(None) == "Без статуса"
assert get_client_tier(-100) == "Без статуса"
assert get_client_tier(1000) == "Новичок"
assert get_client_tier(5000) == "Бронза"
assert get_client_tier(20000) == "Серебро"
assert get_client_tier(50000) == "Золото"
assert get_client_tier(100001) == "Платина"
assert get_client_tier("abc") == "Без статуса"

assert get_client_loyalty_days(None) == 0
assert get_client_loyalty_days("не дата") == 0

print("Все Unit-тесты пройдены!")
