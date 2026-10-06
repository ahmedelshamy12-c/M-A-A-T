"""Messages sent through the Contact Us form.

No Streamlit import: failures are `ValueError`s with user-facing messages.
"""

from services import db

MAX_MESSAGE_LENGTH = 5000


def save_message(user_id, name, email, message):
    """Store a contact message. Raises `ValueError` on invalid input."""
    name = (name or "").strip()
    email = (email or "").strip().lower()
    message = (message or "").strip()

    if not name or not email or not message:
        raise ValueError("Please fill out all fields.")
    if "@" not in email or "." not in email:
        raise ValueError("Please enter a valid email address.")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(
            f"Message is too long (maximum {MAX_MESSAGE_LENGTH} characters)."
        )

    conn = db.get_connection()
    try:
        conn.execute(
            "INSERT INTO contact_messages (user_id, name, email, message) "
            "VALUES (?, ?, ?, ?)",
            (user_id, name, email, message),
        )
        conn.commit()
    finally:
        conn.close()


def list_messages(limit=200):
    """Newest contact messages first, with the sender's username if known."""
    conn = db.get_connection()
    try:
        rows = conn.execute(
            """
            SELECT m.id, m.name, m.email, m.message, m.created_at,
                   u.username
            FROM contact_messages AS m
            LEFT JOIN users AS u ON u.id = m.user_id
            ORDER BY m.created_at DESC, m.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        conn.close()
    return [dict(row) for row in rows]
