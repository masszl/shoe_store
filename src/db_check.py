from db_init import get_connection

conn = get_connection()

tables = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
      AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""").fetchall()

print("Таблицы базы данных:")

for table in tables:
    print(table[0])

print(f"\nВсего таблиц: {len(tables)}")

conn.close()
