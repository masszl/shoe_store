import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "database.db"
BACKUPS = ROOT / "db" / "backups"


def backup_path(prefix):
    BACKUPS.mkdir(parents=True, exist_ok=True)
    return BACKUPS / f"{prefix}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.sqlite"


def backup_simple(source=DB):
    target = backup_path("simple")
    shutil.copy2(source, target)
    return target


def backup_safe(source=DB):
    target = backup_path("safe")
    with sqlite3.connect(source) as src, sqlite3.connect(target) as dst:
        src.backup(dst)
    return target


def restore(backup_file, target=DB):
    backup_file = Path(backup_file)
    target = Path(target)
    if not backup_file.is_file():
        raise FileNotFoundError(backup_file)
    if backup_file.resolve() == target.resolve():
        raise ValueError("Нельзя восстанавливать файл сам в себя")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_file, target)
    return target


def check_integrity(conn):
    return [row[0] for row in conn.execute("PRAGMA integrity_check")]


def get_db_stats(conn):
    size = conn.execute("PRAGMA page_size").fetchone()[0]
    count = conn.execute("PRAGMA page_count").fetchone()[0]
    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]
    return {"page_size": size, "page_count": count, "bytes": size * count, "tables": tables}


def clear_old_logs(conn, days=30):
    result = conn.execute("DELETE FROM audit_log WHERE changed_at < datetime('now', ?)", (f"-{days} days",))
    conn.commit()
    return result.rowcount
