"""Create the Ma`at database.

    python init_db.py            # create data/data_base.db if missing
    python init_db.py --reset    # delete it first, then create it again

Optionally seeds an admin account from ADMIN_EMAIL / ADMIN_PASSWORD /
ADMIN_USERNAME (see .env.example). The database location can be overridden
with the EGY_LAW_DB environment variable.
"""

import argparse

from dotenv import load_dotenv

from services import db
from services.auth_service import ensure_env_admin

def schema_notes(conn):
    """Warn about databases created before `role` existed (CREATE IF NOT EXISTS
    cannot add the column to an existing table)."""
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}
    if "role" in columns:
        return []
    return [
        "Warning: the existing `users` table predates this schema and has no "
        "`role` column.",
        "         Run `python init_db.py --reset` to recreate it "
        "(this deletes every account).",
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Initialise the Ma`at database.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the database file before creating the schema.",
    )
    args = parser.parse_args(argv)

    load_dotenv()

    db_path = db.get_db_path()
    if args.reset and db_path.exists():
        db_path.unlink()
        print(f"Deleted existing database: {db_path}")

    conn = db.get_connection()
    try:
        db.init_schema(conn)
        print(f"Schema applied: {db_path}")
        for note in schema_notes(conn):
            print(note)
        print(ensure_env_admin(conn))
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
