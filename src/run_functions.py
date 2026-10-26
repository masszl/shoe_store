import sqlite3
from pathlib import Path
from app_functions import calc_discount, pluralize_items, format_full_name
from app_functions import (
    calc_discount,
    pluralize_items,
    format_full_name,
    get_client_tier,
    get_client_loyalty_days
)

db_path = Path(__file__).resolve().parent.parent / "db" / "database.db"

conn = sqlite3.connect(db_path)

conn.create_function("calc_discount", 2, calc_discount)
conn.create_function("pluralize_items", 1, pluralize_items)
conn.create_function("format_full_name", 3, format_full_name)
conn.create_function("get_client_tier", 1, get_client_tier)
conn.create_function("get_client_loyalty_days", 1, get_client_loyalty_days)


sql_path = Path(__file__).resolve().parent.parent / "queries" / "10_advanced_queries.sql"

sql_text = sql_path.read_text(encoding="utf-8")
queries = [query.strip() for query in sql_text.split(";") if query.strip()]

for number, query in enumerate(queries, 1):
    print(f"\nЗапрос {number}")
    cursor = conn.execute(query)

    for row in cursor.fetchall():
        print(row)

conn.close()

