"""Single place where the SQLite database is opened.

Every module that talks to the database imports `get_connection` from here, so
the location of the file, the row factory and the foreign-key pragma are
defined in a single module instead of being repeated on every page.
"""

import os
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "data" / "data_base.db"
SCHEMA_PATH = REPO_ROOT / "data" / "schema.sql"

DB_PATH_ENV_VAR = "EGY_LAW_DB"


def get_db_path():
    """Absolute path of the database file.

    Defaults to `<repo>/data/data_base.db` (resolved from this file, so it does
    not depend on the current working directory) and can be pointed somewhere
    else with the `EGY_LAW_DB` environment variable, which is what tests do.
    """
    override = os.environ.get(DB_PATH_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return DEFAULT_DB_PATH


# Database files whose schema has been applied by this process.
_schema_applied = set()


def get_connection():
    """Open the database with `sqlite3.Row` rows and foreign keys enabled.

    The first connection to a given file in this process also applies the
    (idempotent) schema, so a fresh deployment works without `init_db.py`.
    """
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if db_path not in _schema_applied:
        init_schema(conn)
        _schema_applied.add(db_path)
    return conn


def read_schema():
    """Contents of `data/schema.sql`."""
    return SCHEMA_PATH.read_text(encoding="utf-8")


def init_schema(conn):
    """Apply `data/schema.sql` to an open connection (idempotent)."""
    conn.executescript(read_schema())
    conn.commit()
