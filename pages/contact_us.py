import streamlit as st

st.set_page_config(page_title="Contact Us", layout="centered")




st.title("Contact Us")
st.write("If you have any questions or inquiries, feel free to contact us — we're here to help.")



if st.session_state.logged_user is None:
    
    st.warning("You must be logged in to access the chat.")
    st.stop()


    
# Contact info
st.subheader("Contact Information")
st.write("📧 Email: ahedmedhat@gmail.com")
st.write("📞 Phone: +20 1008096453")
st.write("📍 Address: Cairo, Egypt")

st.divider()

# Contact form
name = st.text_input("Name")
email = st.text_input("Email")
message = st.text_area("Message")

if st.button("Send"):
    if name and email and message:
        st.success("Thank you for your message!")
    else:
        st.error("Please fill out all fields.")
