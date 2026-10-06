import streamlit as st

from services.contact_service import save_message
from services.session import require_login

st.set_page_config(page_title="Contact Us", layout="centered")

st.title("Contact Us")
st.write("If you have any questions or inquiries, feel free to contact us — we're here to help.")

user = require_login()

# Contact info
st.subheader("Contact Information")
st.write("📧 Email: ahedmedhat@gmail.com")
st.write("📞 Phone: +20 1008096453")
st.write("📍 Address: Cairo, Egypt")

st.divider()

# Contact form — messages are stored and shown to admins on the View Users page.
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Name", value=user["username"])
    email = st.text_input("Email", value=user["email"])
    message = st.text_area("Message")
    sent = st.form_submit_button("Send")

if sent:
    try:
        save_message(user["id"], name, email, message)
    except ValueError as error:
        st.error(str(error))
    except Exception as error:
        st.error(f"Your message couldn't be sent: {error}")
    else:
        st.success("Thank you for your message! We'll get back to you soon.")
