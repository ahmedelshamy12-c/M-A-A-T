import streamlit as st
from services.auth_service import register, login


st.set_page_config(page_title="Auth", page_icon="🔐")


st.title("🔐Enter Gate ")

if st.session_state.get("logged_user") is not None:
    user = st.session_state.logged_user
    st.success(f"Logged in as {user['username']}")
    if st.button("Go to chat", type="primary"):
        st.switch_page("pages/chat.py")
    st.stop()


tab1, tab2 = st.tabs(["Log in", "Create Account/register"])

with tab1:


    st.subheader("Log in")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        
        if st.form_submit_button("Login", use_container_width=True):
            

            user = login(email, password)
            
            if user:
                st.success("Login successful!")
                st.session_state.logged_user = user
                st.switch_page("pages/chat.py")
            else:
                st.error("Invalid login credentials.")



with tab2: 
    
    st.subheader("Create New Account")
    
   
    with st.form("signup_form"):
        

        col1, col2 = st.columns(2)
        with col1:  
            username = st.text_input("Choose Username")
            email = st.text_input("Email")
            ssn = st.text_input("National ID (14 digits)")


        with col2:  
            password = st.text_input("Password", type="password")
            job = st.text_input("Job")
            age = st.number_input("Age", min_value=18, max_value=120, step=1, value=18)
    
    
        if st.form_submit_button("Create Account", use_container_width=True):


            try:
                register(username, email, password, ssn, job, age)
            except ValueError as error:
                st.error(str(error))
            else:
                st.success("Account created — you can now log in.")
