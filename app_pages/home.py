import streamlit as st

st.title("⚖️ Ma`at")
st.subheader("A smart helper for understanding Egyptian legal documents")

st.info(
    "This app gives general information only. "
    "It is not a replacement for advice from a real lawyer."
)







col1, col2, col3 = st.columns(3)



with col1:
    with st.container(border=True):
        st.markdown("### :material/upload_file: Upload")
        st.write("Upload a law, a contract or a court ruling as a PDF.")


with col2:
    with st.container(border=True):
        st.markdown("### :material/forum: Ask")
        st.write("Ask questions in Arabic or English and get answers from your file.")


with col3:
    with st.container(border=True):
        st.markdown("### :material/summarize: Summarize")
        st.write("Get a short, simple summary of the whole document.")



if "user" not in st.session_state:
    st.write("To get started, log in or create an account.")
    if st.button("Log in / Sign up", type="primary"):
        st.switch_page("app_pages/login.py")


else:
    if st.button("Go to the chat", type="primary"):
        st.switch_page("app_pages/chat.py")
