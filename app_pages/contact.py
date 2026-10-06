import streamlit as st

from services.contact_service import add_contact_message

if "user" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

user = st.session_state.user

st.title("Contact us")
st.write("Have a question? We're happy to help.")

with st.container(border=True):
    st.write(":material/mail: ahedmedhat@gmail.com")
    st.write(":material/call: +20 1008096453")
    st.write(":material/location_on: Cairo, Egypt")

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Name", value=user["username"])
    email = st.text_input("Email", value=user["email"])
    message = st.text_area("Message")
    send_clicked = st.form_submit_button("Send", type="primary")

if send_clicked:
    if name == "" or email == "" or message == "":
        st.error("Please fill in all the boxes.")
    else:
        add_contact_message(user["id"], name, email, message)
        st.success("Thank you! Your message was sent.")
