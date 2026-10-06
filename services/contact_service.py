# Messages sent from the Contact us page.

from services.database import connect


def add_contact_message(user_id, name, email, message):
    connection = connect()
    connection.execute(
        "INSERT INTO contact_messages (user_id, name, email, message) "
        "VALUES (?, ?, ?, ?)",
        (user_id, name, email, message),
    )
    connection.commit()
    connection.close()


def get_contact_messages():
    connection = connect()
    rows = connection.execute(
        "SELECT name, email, message, created_at FROM contact_messages "
        "ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]
