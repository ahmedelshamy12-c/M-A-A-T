"""Shared page guard.

Pages call `require_login()` at the top instead of poking at
`st.session_state.logged_user` themselves, so the "not logged in" path never
raises `AttributeError` and every protected page gets the same logout button.
"""

import streamlit as st

USER_KEY = "logged_user"
# Session-only data that must not survive a logout.
VOLATILE_KEYS = ("messages", "vectorstore")


def require_login(admin: bool = False):
    """Stop the page render unless someone is logged in (and is an admin).

    Returns the logged-in user dict: `id`, `username`, `email`, `role`.
    """
    user = st.session_state.get(USER_KEY)

    if user is None:
        st.warning("You must be logged in to view this page.")
        st.page_link("pages/auth.py", label="Log in / Create account")
        st.stop()

    if admin and user.get("role") != "admin":
        st.error("Admins only.")
        st.stop()

    _render_sidebar(user)
    return user


def log_out():
    """Drop the session's user and cached chat/document state."""
    for key in (USER_KEY,) + VOLATILE_KEYS:
        st.session_state.pop(key, None)
    st.switch_page("app.py")


def _render_sidebar(user):
    with st.sidebar:
        st.markdown("---")
        st.write(f"Logged in as {user['username']}")
        if st.button("Log out", use_container_width=True):
            log_out()
