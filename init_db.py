"""Create the Ma`at database.

    python init_db.py            # create data/data_base.db if missing
    python init_db.py --reset    # delete it first, then create it again

Optionally seeds an admin account from ADMIN_EMAIL / ADMIN_PASSWORD /
ADMIN_USERNAME (see .env.example). The database location can be overridden
with the EGY_LAW_DB environment variable.
"""

import argparse
import os

from dotenv import load_dotenv

from services import db
from services.auth_service import hash_password

DEFAULT_ADMIN_USERNAME = "admin"


def create_admin(conn):
    """Create the admin user from env vars if it is missing. Returns a log line."""
    email = (os.environ.get("ADMIN_EMAIL") or "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD") or ""
    username = (os.environ.get("ADMIN_USERNAME") or "").strip() or DEFAULT_ADMIN_USERNAME

    if not email or not password:
        return "No admin created: set ADMIN_EMAIL and ADMIN_PASSWORD in .env."

    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?", (email,)
    ).fetchone()
    if existing is not None:
        return f"Admin already exists for {email} (id={existing['id']}); left unchanged."

    conn.execute(
        """
        INSERT INTO users (username, email, password, job, age, ssn, role)
        VALUES (?, ?, ?, NULL, NULL, NULL, 'admin')
        """,
        (username, email, hash_password(password)),
    )
    conn.commit()
    return f"Created admin: username={username} email={email}"


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
        print(create_admin(conn))
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
