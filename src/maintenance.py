import sqlite3
from pathlib import Path
from admin import install_roles, test_permissions
from backup_restore import DB, backup_simple, backup_safe, restore, check_integrity, get_db_stats, clear_old_logs


def main():
    if not DB.is_file():
        raise FileNotFoundError(f"База не найдена: {DB}")
    with sqlite3.connect(DB) as conn:
        print("Целостность:", check_integrity(conn))
        print("Статистика:", get_db_stats(conn))
        test_permissions(conn)
    simple = backup_simple()
    safe = backup_safe()
    print("Обычная копия:", simple)
    print("Безопасная копия:", safe)
    with sqlite3.connect(DB) as conn:
        has_audit = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='audit_log'").fetchone()
        if has_audit:
            print("Удалено старых логов:", clear_old_logs(conn))
    demo = DB.parent / "restore_demo.sqlite"
    restore(safe, demo)
    with sqlite3.connect(demo) as conn:
        before = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        conn.execute("PRAGMA foreign_keys=OFF")
        conn.execute("DELETE FROM order_items")
        conn.execute("DELETE FROM orders")
        conn.commit()
        damaged = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    restore(safe, demo)
    with sqlite3.connect(demo) as conn:
        after = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    print(f"Восстановление заказов: до={before}, после удаления={damaged}, после восстановления={after}")
    assert before == after and damaged == 0
    try:
        demo.unlink()
    except PermissionError:
        print("Тестовая база занята, пропускаем удаление")
    conn.close()
    print("День 12: готово")


if __name__ == "__main__":
    main()
