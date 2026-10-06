# Ma`at — the start of the app.
# It makes the database tables and decides which pages the menu shows.

import streamlit as st

from services.database import create_tables

st.set_page_config(page_title="Ma`at", page_icon="⚖️", layout="wide")

create_tables()

home = st.Page("app_pages/home.py", title="Home", icon=":material/home:")
login = st.Page("app_pages/login.py", title="Log in", icon=":material/login:")
chat = st.Page("app_pages/chat.py", title="Chat", icon=":material/chat:", default=True)
contact = st.Page("app_pages/contact.py", title="Contact us", icon=":material/mail:")
admin = st.Page("app_pages/admin.py", title="Admin", icon=":material/shield_person:")
logout = st.Page("app_pages/logout.py", title="Log out", icon=":material/logout:")

# Before logging in you only see Home and Log in.
# After logging in you see the chat; the admin also sees the Admin page.
if "user" not in st.session_state:
    pages = [home, login]
elif st.session_state.user["role"] == "admin":
    pages = [chat, home, contact, admin, logout]
else:
    pages = [chat, home, contact, logout]

page = st.navigation(pages, position="top")
page.run()
