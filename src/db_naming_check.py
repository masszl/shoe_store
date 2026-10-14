import re
from db_init import get_connection


RESERVED_WORDS = {
    "select", "from", "where", "table", "index",
    "order", "group", "insert", "update", "delete",
    "create", "drop", "join", "primary", "key"
}


def get_tables(conn):
    result = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    return [row[0] for row in result]


def get_columns(conn, table_name):
    result = conn.execute(
        f'PRAGMA table_info("{table_name}")'
    ).fetchall()

    return [row[1] for row in result]


def check_name(name):
    errors = []

    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        errors.append("Неверный формат имени")

    if name.lower() in RESERVED_WORDS:
        errors.append("Зарезервированное слово SQL")

    return errors


def check_database():
    conn = get_connection()
    errors_count = 0

    try:
        tables = get_tables(conn)

        for table in tables:
            table_errors = check_name(table)

            if not table.endswith("s"):
                table_errors.append("Название таблицы не во множественном числе")

            if table_errors:
                print(f"[FAIL] Таблица {table}: {', '.join(table_errors)}")
                errors_count += len(table_errors)
            else:
                print(f"[PASS] Таблица {table}")

            for column in get_columns(conn, table):
                column_errors = check_name(column)

                if column_errors:
                    print(f"[FAIL] Поле {table}.{column}: {', '.join(column_errors)}")
                    errors_count += len(column_errors)
                else:
                    print(f"[PASS] Поле {table}.{column}")

        print(f"\nПроверено таблиц: {len(tables)}")
        print(f"Найдено ошибок: {errors_count}")

    finally:
        conn.close()


if __name__ == "__main__":
    check_database()
