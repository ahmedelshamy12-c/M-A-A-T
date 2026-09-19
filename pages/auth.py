import streamlit as st
import sqlite3
from services.auth_service import register, login


st.set_page_config(page_title="Auth", page_icon="🔐")


st.title("🔐Enter Gate ")

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
            ssn = st.text_input("SSN")


        with col2:  
            password = st.text_input("Password", type="password")
            job = st.text_input("Job")
            age = st.text_input("Age")
    
    
        if st.form_submit_button("Create Account", use_container_width=True):


            register(username, email, password, ssn, job, age)

            st.success("Account created successfully!")
