# Signing up and logging in users.

from services.database import connect


def username_or_email_taken(username, email):
    connection = connect()
    user = connection.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?", (username, email)
    ).fetchone()
    connection.close()
    return user is not None


def add_user(username, email, password, ssn, job, age):
    connection = connect()
    count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    # The very first person who signs up becomes the admin.
    if count == 0:
        role = "admin"
    else:
        role = "user"

    connection.execute(
        "INSERT INTO users (username, email, password, ssn, job, age, role) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (username, email, password, ssn, job, age, role),
    )
    connection.commit()
    connection.close()


def find_user(email, password):
    connection = connect()
    user = connection.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
    ).fetchone()
    connection.close()
    if user is None:
        return None
    return dict(user)


def get_all_users():
    connection = connect()
    users = connection.execute(
        "SELECT username, email, job, age, role, created_at FROM users"
    ).fetchall()
    connection.close()
    return [dict(user) for user in users]
