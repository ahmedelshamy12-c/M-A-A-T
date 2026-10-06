# Saving chats and their messages.

from services.database import connect


def new_chat(user_id, title):
    connection = connect()
    cursor = connection.execute(
        "INSERT INTO chats (user_id, title) VALUES (?, ?)", (user_id, title)
    )
    connection.commit()
    chat_id = cursor.lastrowid
    connection.close()
    return chat_id


def add_message(chat_id, sender, text):
    connection = connect()
    connection.execute(
        "INSERT INTO messages (chat_id, sender, text) VALUES (?, ?, ?)",
        (chat_id, sender, text),
    )
    connection.commit()
    connection.close()


def get_chats(user_id):
    connection = connect()
    chats = connection.execute(
        "SELECT id, title FROM chats WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    connection.close()
    return [dict(chat) for chat in chats]


def get_messages(chat_id):
    connection = connect()
    rows = connection.execute(
        "SELECT sender, text FROM messages WHERE chat_id = ? ORDER BY id", (chat_id,)
    ).fetchall()
    connection.close()
    messages = []
    for row in rows:
        messages.append({"role": row["sender"], "content": row["text"]})
    return messages
