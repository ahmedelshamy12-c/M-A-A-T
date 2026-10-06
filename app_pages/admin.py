import streamlit as st



from services.contact_service import get_contact_messages
from services.user_service import get_all_users



if "user" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()



if st.session_state.user["role"] != "admin":
    st.error("Only the admin can see this page.")
    st.stop()





st.title("Admin")




users_tab, messages_tab = st.tabs(["Users", "Contact messages"])




with users_tab:
    users = get_all_users()
    st.write("Number of users:", len(users))
    st.dataframe(users, hide_index=True)




with messages_tab:
    messages = get_contact_messages()
    if len(messages) == 0:
        st.info("No messages yet.")
    for message in messages:
        with st.container(border=True):
            st.markdown(f"**{message['name']}** ({message['email']})")
            st.caption(message["created_at"])
            st.write(message["message"])
