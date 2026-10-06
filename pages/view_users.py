import streamlit as st

from services import db
from services.contact_service import list_messages
from services.session import require_login

st.set_page_config(page_title="View Users", page_icon="📊", layout="wide")

st.title("View Users")



require_login(admin=True)

conn = None
try:
    conn = db.get_connection()

    rows = conn.execute("""
    SELECT
        username,
        email,
        role,
        ssn,
        job,
        age
    FROM users
    ORDER BY created_at DESC
    """).fetchall()

    users = [dict(row) for row in rows]
except Exception as e:
    st.error(f"Failed to load users: {e}")
    users = []
finally:
    if conn:
        conn.close()


def mask_ssn(ssn):
    if not ssn:
        return "—"
    return "*" * 10 + str(ssn)[-4:]


try:
    contact_messages = list_messages()
except Exception as e:
    st.error(f"Failed to load contact messages: {e}")
    contact_messages = []

users_tab, messages_tab = st.tabs(
    [f"Users ({len(users)})", f"Contact messages ({len(contact_messages)})"]
)

with users_tab:
    if not users:
        st.info("No users found.")
    else:
        cols = st.columns(3)
        for i, user in enumerate(users):

            with cols[i % 3]:
                with st.container():
                    st.header(user["username"])

                    st.text(f"Email: {user['email']}")
                    st.text(f"Role: {user['role']}")
                    st.text(f"Job: {user['job'] or '—'}")
                    st.text(f"Age: {user['age'] if user['age'] is not None else '—'}")
                    st.text(f"National ID: {mask_ssn(user['ssn'])}")

with messages_tab:
    if not contact_messages:
        st.info("No contact messages yet.")
    for item in contact_messages:
        with st.container(border=True):
            account = f" · account: {item['username']}" if item["username"] else ""
            st.caption(f"{item['created_at']} · {item['email']}{account}")
            st.markdown(f"**{item['name']}**")
            st.text(item["message"])
