
import streamlit as st
import sqlite3

st.set_page_config(page_title="View Users", page_icon="📊", layout="wide")

st.title("View Users")



if st.session_state.logged_user is None:
    
    st.warning("You must be logged in to access the chat.")
    st.stop()

conn = None
try:
    conn = sqlite3.connect("data/data_base.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        username,
        email,
        ssn,
        job,
        age
    FROM users
    ORDER BY created_at DESC
    """)

    users = cursor.fetchall()
except Exception as e:
    st.error(f"Failed to load users: {e}")
    users = []
finally:
    if conn:
        conn.close()

if not users:
    st.info("No users found.")
else:
    cols = st.columns(3)
    for i, user in enumerate(users):
        username, email, ssn, job, age = user

        with cols[i % 3]:
            with st.container():
                st.header(username)

                st.text(f"Email: {email}")
                st.text(f"Job: {job}")
                st.text(f"Age: {age}")
                st.text(f"SSN: {ssn}")


                st.button("View details", use_container_width=True, key=f"view_details_{i}")