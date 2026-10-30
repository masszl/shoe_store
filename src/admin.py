import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "database.db"
PERMISSIONS = {
    "admin_db": {"SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"},
    "developer": {"SELECT", "INSERT", "UPDATE"},
    "reader": {"SELECT"},
}


def install_roles(conn):
    columns = {row[1] for row in conn.execute("PRAGMA table_info(roles)")}
    name_column = next((x for x in ("role_name", "name") if x in columns), None)
    if name_column is None:
        raise RuntimeError(f"Не найден столбец имени роли: {columns}")
    for role in PERMISSIONS:
        conn.execute(f"INSERT INTO roles ({name_column}) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM roles WHERE {name_column} = ?)", (role, role))
    conn.commit()
    return name_column


def check_permission(conn, user_id, action):
    columns = {row[1] for row in conn.execute("PRAGMA table_info(roles)")}
    name_column = next((x for x in ("role_name", "name") if x in columns), None)
    if name_column is None:
        return False
    row = conn.execute(f"SELECT r.{name_column} FROM users u JOIN roles r ON r.role_id = u.role_id WHERE u.user_id = ?", (user_id,)).fetchone()
    return bool(row and action.upper() in PERMISSIONS.get(row[0], set()))


def test_permissions(conn):
    role_column = install_roles(conn)
    for role in ("reader", "admin_db"):
        row = conn.execute(f"SELECT u.user_id FROM users u JOIN roles r ON r.role_id = u.role_id WHERE r.{role_column} = ? LIMIT 1", (role,)).fetchone()
        if row:
            print(f"{role}: DELETE = {check_permission(conn, row[0], 'DELETE')}")
        else:
            print(f"{role}: пользователь не назначен; проверка пропущена")


if __name__ == "__main__":
    with sqlite3.connect(DB) as conn:
        test_permissions(conn)
