import streamlit as st




from services.ai_service import answer_question, embed, find_best_parts, summarize
from services.chat_service import add_message, get_chats, get_messages, new_chat
from services.pdf_service import MAX_PARTS, read_pdf, split_text

# Questions the user can ask with one click, and the color of each one.
QUESTION_COLORS = {
    "What is this document about?": "blue",
    "What are my rights?": "green",
    "What are my duties?": "orange",
    "Are there any deadlines or dates?": "violet",
    "Are there any penalties or fines?": "red",
    "Explain it in simple words": "gray",
}
SUGGESTED_QUESTIONS = list(QUESTION_COLORS)  # just the questions






if "user" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()



user = st.session_state.user





# Things we remember while the user is on the site.
if "messages" not in st.session_state:
    st.session_state.messages = []  # the chat on the screen
    st.session_state.chat_id = None  # the saved chat in the database
    st.session_state.pdf_name = None
    st.session_state.pdf_text = ""
    st.session_state.parts = []  # the PDF cut into parts
    st.session_state.vectors = []  # the embedding of every part
    st.session_state.suggested_question = None  # a question picked from the pills





def colored(question):
    # Show the question in its own color, e.g. ":green[What are my rights?]"
    return ":" + QUESTION_COLORS[question] + "[" + question + "]"


def use_suggestion():
    # Remember the question that was clicked, then un-select the pill
    # so the same question can be clicked again later.
    st.session_state.suggested_question = st.session_state.suggestion
    st.session_state.suggestion = None


def save(role, text):
    # Show the message now and save it in the database.
    if st.session_state.chat_id is None:
        title = text[:40]
        st.session_state.chat_id = new_chat(user["id"], title)
    st.session_state.messages.append({"role": role, "content": text})
    add_message(st.session_state.chat_id, role, text)





# ---------- The sidebar: the PDF and the saved chats ----------

with st.sidebar:
    st.header("Your document")
    pdf_file = st.file_uploader("Upload a PDF", type="pdf")

    if pdf_file is not None and pdf_file.name != st.session_state.pdf_name:
        text = read_pdf(pdf_file)
        parts = split_text(text)

        if len(parts) == 0:
            st.error("This PDF has no text we can read (maybe it is a scan).")
        elif len(parts) > MAX_PARTS:
            st.error(f"This PDF is too big. The limit is {MAX_PARTS} parts.")
        else:
            with st.spinner("Reading your document..."):
                st.session_state.vectors = embed(parts)
            st.session_state.parts = parts
            st.session_state.pdf_text = text
            st.session_state.pdf_name = pdf_file.name

    if st.session_state.pdf_name:
        st.success(f"Ready: {st.session_state.pdf_name}")
        if st.button("Summarize the document", icon=":material/summarize:"):
            save("user", "Summarize " + st.session_state.pdf_name)
            with st.spinner("Writing the summary..."):
                summary = summarize(st.session_state.pdf_text)
            save("assistant", summary)
    else:
        st.caption("No document yet. Answers will use general knowledge.")

    st.divider()
    st.header("Your chats")

    if st.button("New chat", icon=":material/add:"):
        st.session_state.messages = []
        st.session_state.chat_id = None

    for chat in get_chats(user["id"]):
        if st.button(chat["title"], key=f"chat_{chat['id']}"):
            st.session_state.chat_id = chat["id"]
            st.session_state.messages = get_messages(chat["id"])









# ---------- The main part: the conversation ----------

st.title("What do you want to ask today?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.pills(
    "Suggested questions",
    SUGGESTED_QUESTIONS,
    format_func=colored,
    key="suggestion",
    on_change=use_suggestion,
)

question = st.chat_input("Ask a question about your document...")

# A clicked pill counts as a question too.
if st.session_state.get("suggested_question"):
    question = st.session_state.suggested_question
    st.session_state.suggested_question = None

if question:
    with st.chat_message("user"):
        st.markdown(question)

    best_parts = []
    if st.session_state.parts:
        best_parts = find_best_parts(
            question, st.session_state.parts, st.session_state.vectors
        )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = answer_question(question, best_parts)
        st.markdown(answer)

    save("user", question)
    save("assistant", answer)
    st.rerun()  # so the new chat appears in the sidebar
