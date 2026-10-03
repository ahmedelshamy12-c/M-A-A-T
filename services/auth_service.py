"""Sign-up and log-in logic.

Deliberately free of any Streamlit import so it can be unit-tested (and driven
from `init_db.py`) without a UI. All failures are reported as `ValueError` with
a message that is safe to show to the user.
"""

import hashlib
import hmac
import secrets
import sqlite3

from services import db

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16
MIN_PASSWORD_LENGTH = 8
SSN_LENGTH = 14
MIN_AGE = 18
MAX_AGE = 120


def hash_password(password):
    """Hash `password` with PBKDF2-HMAC-SHA256.

    Returns `pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>`.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )
    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password, stored):
    """Check `password` against a stored hash. Never raises on a bad hash."""
    if not isinstance(password, str) or not isinstance(stored, str):
        return False

    parts = stored.split("$")
    if len(parts) != 4:
        return False

    algorithm, iterations_text, salt_hex, hash_hex = parts
    if algorithm != ALGORITHM:
        return False

    try:
        iterations = int(iterations_text)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
    except ValueError:
        return False

    if iterations <= 0 or not salt:
        return False

    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return hmac.compare_digest(candidate, expected)


def _clean(value):
    return "" if value is None else str(value).strip()


def _parse_age(age):
    try:
        return int(_clean(age))
    except ValueError:
        raise ValueError(
            "Age is required and must be a whole number between "
            f"{MIN_AGE} and {MAX_AGE}."
        ) from None


def _validate(username, email, password, ssn, age):
    if not username:
        raise ValueError("Username is required.")
    if not email:
        raise ValueError("Email is required.")
    if "@" not in email or "." not in email:
        raise ValueError("Please enter a valid email address.")
    if not password:
        raise ValueError("Password is required.")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
        )
    if not ssn:
        raise ValueError("National ID is required.")
    if not (len(ssn) == SSN_LENGTH and ssn.isdigit()):
        raise ValueError(f"National ID must be exactly {SSN_LENGTH} digits.")

    age_value = _parse_age(age)
    if not (MIN_AGE <= age_value <= MAX_AGE):
        raise ValueError(
            f"Age must be a whole number between {MIN_AGE} and {MAX_AGE}."
        )
    return age_value


_DUPLICATE_MESSAGES = (
    ("username", "This username is already registered."),
    ("email", "This email is already registered."),
    ("ssn", "This national ID is already registered."),
)


def _duplicate_message(error):
    text = str(error)
    for column, message in _DUPLICATE_MESSAGES:
        if column in text:
            return message
    return "This account is already registered."


def register(username, email, password, ssn, job, age):
    """Create a `user` account. Raises `ValueError` on any invalid input."""
    username = _clean(username)
    email = _clean(email).lower()
    password = _clean(password)
    ssn = _clean(ssn)
    job = _clean(job) or None

    age_value = _validate(username, email, password, ssn, age)

    conn = db.get_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (username, email, password, job, age, ssn, role)
            VALUES (?, ?, ?, ?, ?, ?, 'user')
            """,
            (username, email, hash_password(password), job, age_value, ssn),
        )
        conn.commit()
    except sqlite3.IntegrityError as error:
        raise ValueError(_duplicate_message(error)) from error
    finally:
        conn.close()


def login(email, password):
    """Return the session dict for valid credentials, otherwise `None`."""
    email = _clean(email).lower()
    password = _clean(password)
    if not email or not password:
        return None

    conn = db.get_connection()
    try:
        row = conn.execute(
            "SELECT id, username, email, password, role FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return None
    if not verify_password(password, row["password"]):
        return None

    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "role": row["role"],
    }
