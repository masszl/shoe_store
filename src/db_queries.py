from pathlib import Path
from db_init import get_connection

query_path = Path(__file__).resolve().parent.parent / "queries" / "02_check_queries.sql"

sql = query_path.read_text(encoding="utf-8")
queries = [query.strip() for query in sql.split(";") if query.strip()]

conn = get_connection()

for number, query in enumerate(queries, start=1):
    print(f"\nЗапрос №{number}")

    cursor = conn.execute(query)
    print(" | ".join(column[0] for column in cursor.description))

    for row in cursor.fetchall():
        print(" | ".join(str(value) for value in row))

conn.close()
