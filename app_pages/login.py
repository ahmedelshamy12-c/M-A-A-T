import streamlit as st

from services.user_service import add_user, find_user, username_or_email_taken

st.title("Welcome")

login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

with login_tab:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_clicked = st.form_submit_button("Log in", type="primary")

    if login_clicked:
        user = find_user(email, password)
        if user is None:
            st.error("Wrong email or password.")
        else:
            st.session_state.user = user
            st.rerun()  # the menu now shows the chat

with signup_tab:
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        ssn = st.text_input("National ID")
        job = st.text_input("Job")
        age = st.number_input("Age", min_value=18, max_value=120, value=18)
        signup_clicked = st.form_submit_button("Create account", type="primary")

    if signup_clicked:
        if username == "" or email == "" or password == "" or ssn == "":
            st.error("Please fill in username, email, password and national ID.")
        elif username_or_email_taken(username, email):
            st.error("This username or email is already used.")
        else:
            add_user(username, email, password, ssn, job, age)
            st.success("Your account is ready! Now log in.")
