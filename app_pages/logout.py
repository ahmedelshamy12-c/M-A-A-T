import streamlit as st

# Forget everything about this user, then go back to the home page.
st.session_state.clear()
st.rerun()
