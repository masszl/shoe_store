import sqlite3
from pathlib import Path
from admin import install_roles
from auth_secure import prepare_auth, register_user, check_password
from security_demo import run_demo

DB = Path(__file__).resolve().parent.parent / "db" / "database.db"


def main():
    if not DB.is_file():
        raise FileNotFoundError(DB)
    with sqlite3.connect(DB) as source, sqlite3.connect(":memory:") as conn:
        source.backup(conn)
        conn.execute("PRAGMA foreign_keys=ON")
        install_roles(conn)
        prepare_auth(conn)
        run_demo(conn)
        login = "day13_test_user"
        register_user(conn, login, "admin123")
        good = check_password(conn, login, "admin123")
        bad = check_password(conn, login, "wrong")
        print("Правильный пароль:", good)
        print("Неправильный пароль:", bad)
        assert good and not bad
        print("Аудит входов:", conn.execute("SELECT login, status FROM login_audit WHERE login=?", (login,)).fetchall())
    with sqlite3.connect(DB) as conn:
        prepare_auth(conn)
    print("День 13: готово")


if __name__ == "__main__":
    main()
