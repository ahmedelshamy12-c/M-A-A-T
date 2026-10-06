"""Saved conversations (the `Conversations` and `Messages` tables).

Every function takes the owner's `user_id` and only touches that user's
conversations, so one user can never read or delete another user's chats.
Messages are stored with sender `user` or `assistant`, matching the roles the
chat page renders.
"""

from services import db

TITLE_LENGTH = 60


def make_title(first_question):
    """Short conversation title from the first question."""
    title = " ".join((first_question or "").split())
    if len(title) > TITLE_LENGTH:
        title = title[: TITLE_LENGTH - 1].rstrip() + "…"
    return title or "New chat"


def create_conversation(user_id, title):
    """Create an empty conversation and return its id."""
    conn = db.get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO Conversations (user_id, title) VALUES (?, ?)",
            (user_id, title),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def add_message(conversation_id, user_id, sender, text):
    """Append a message to one of the user's conversations."""
    if sender not in ("user", "assistant"):
        raise ValueError(f"Unknown sender: {sender!r}")

    conn = db.get_connection()
    try:
        owned = conn.execute(
            "SELECT 1 FROM Conversations WHERE id = ? AND user_id = ?",
            (conversation_id, user_id),
        ).fetchone()
        if owned is None:
            raise ValueError("Conversation not found.")
        conn.execute(
            "INSERT INTO Messages (conversation_id, sender, message) "
            "VALUES (?, ?, ?)",
            (conversation_id, sender, text),
        )
        conn.commit()
    finally:
        conn.close()


def list_conversations(user_id, limit=30):
    """The user's conversations, most recently active first."""
    conn = db.get_connection()
    try:
        rows = conn.execute(
            """
            SELECT c.id, c.title, c.created_at,
                   COALESCE(MAX(m.created_at), c.created_at) AS last_active
            FROM Conversations AS c
            LEFT JOIN Messages AS m ON m.conversation_id = c.id
            WHERE c.user_id = ?
            GROUP BY c.id
            ORDER BY last_active DESC, c.id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()
    return [dict(row) for row in rows]


def get_messages(conversation_id, user_id):
    """Messages of one of the user's conversations as chat-page dicts.

    Returns `[]` if the conversation doesn't exist or belongs to someone else.
    """
    conn = db.get_connection()
    try:
        rows = conn.execute(
            """
            SELECT m.sender, m.message
            FROM Messages AS m
            JOIN Conversations AS c ON c.id = m.conversation_id
            WHERE c.id = ? AND c.user_id = ?
            ORDER BY m.id
            """,
            (conversation_id, user_id),
        ).fetchall()
    finally:
        conn.close()
    return [{"role": row["sender"], "content": row["message"]} for row in rows]


def delete_conversation(conversation_id, user_id):
    """Delete one of the user's conversations and its messages."""
    conn = db.get_connection()
    try:
        owned = conn.execute(
            "SELECT 1 FROM Conversations WHERE id = ? AND user_id = ?",
            (conversation_id, user_id),
        ).fetchone()
        if owned is None:
            return
        conn.execute(
            "DELETE FROM Messages WHERE conversation_id = ?", (conversation_id,)
        )
        conn.execute("DELETE FROM Conversations WHERE id = ?", (conversation_id,))
        conn.commit()
    finally:
        conn.close()
