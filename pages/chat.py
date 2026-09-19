import streamlit as st
import sqlite3

st.title("what do you want to ask today?")





if st.session_state.logged_user is None:
    st.session_state.logged_user = None
    st.warning("You must be logged in to access the chat.")
    st.stop()


st.chat_input("Type your message here...")

st.sidebar.title("Chat Sidebar")
st.sidebar.write("documents")
st.sidebar.write("chat history")

with st.sidebar.form("upload_doc"):
    uploaded_file = st.file_uploader("Upload Document")
    submit = st.form_submit_button("Upload", use_container_width=True)
    if submit and uploaded_file is not None:
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")


