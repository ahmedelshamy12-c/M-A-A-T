import streamlit as st

from services import chat_history
from services.documents_service import (
    RATE_LIMIT_MESSAGE,
    get_pdf_text,
    index_text,
    is_rate_limit,
)
from services.llm_service import get_ai_response, summarize_documents
from services.session import require_login

CHAT_INPUT_PLACEHOLDER = "Ask a question about your documents..."

# `unicode-bidi: plaintext` makes each block take its direction from its first
# strong character and `text-align: start` then aligns it accordingly: Arabic
# paragraphs go right-to-left, English ones left-to-right, and a paragraph that
# mixes both is still laid out from the correct side.
CHAT_DIRECTION_CSS = (
    "<style>[data-testid='stChatMessage'] :is(p, li, h1, h2, h3, h4, "
    "blockquote) { unicode-bidi: plaintext; text-align: start; }</style>"
)

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

st.markdown(CHAT_DIRECTION_CSS, unsafe_allow_html=True)

st.session_state.setdefault("messages", [])
st.session_state.setdefault("vectorstore", None)
st.session_state.setdefault("doc_names", [])
st.session_state.setdefault("doc_text", "")
st.session_state.setdefault("conversation_id", None)

user = require_login()


def remember(role, content, title_source=None):
    """Add a message to the visible chat and save it to the user's history.

    The first message of a new chat creates the conversation, titled from
    `title_source` (or the message itself). A failed save is reported but
    doesn't interrupt the chat.
    """
    st.session_state.messages.append({"role": role, "content": content})
    try:
        if st.session_state.conversation_id is None:
            st.session_state.conversation_id = chat_history.create_conversation(
                user["id"], chat_history.make_title(title_source or content)
            )
        chat_history.add_message(
            st.session_state.conversation_id, user["id"], role, content
        )
    except Exception as e:
        st.warning(f"This message couldn't be saved to your history: {e}")


def start_new_chat():
    st.session_state.messages = []
    st.session_state.conversation_id = None


with st.sidebar:
    st.header("Documents")

    with st.form("upload_form"):
        uploaded_files = st.file_uploader(
            "Upload PDF documents", type=["pdf"], accept_multiple_files=True
        )
        submitted = st.form_submit_button(
            "Process documents", use_container_width=True
        )

    if submitted and uploaded_files:
        try:
            with st.spinner("Reading and indexing documents..."):
                text = get_pdf_text(uploaded_files)
                bar = st.progress(0.0, text="Indexing...")
                vectorstore = index_text(
                    text,
                    progress=lambda done: bar.progress(
                        done, text=f"Indexing... {done:.0%}"
                    ),
                )
                bar.empty()

            if vectorstore is None:
                st.error(
                    "No readable text found in these PDFs "
                    "(scanned images aren't supported)."
                )
            else:
                st.session_state.vectorstore = vectorstore
                st.session_state.doc_text = text
                st.session_state.doc_names = [file.name for file in uploaded_files]
                st.success(
                    f"Indexed {len(st.session_state.doc_names)} document(s)."
                )
        except Exception as e:
            reason = RATE_LIMIT_MESSAGE if is_rate_limit(e) else str(e)
            st.error(f"Could not process the documents: {reason}")

    doc_names = st.session_state.doc_names
    if doc_names:
        st.subheader("Loaded documents")
        for name in doc_names:
            st.markdown(f"- {name}")
    else:
        st.caption("No documents loaded — answers will use general knowledge.")

    if st.button(
        "Summarize documents",
        use_container_width=True,
        type="primary",
        disabled=not st.session_state.doc_text,
    ):
        names = ", ".join(doc_names)
        remember(
            "user",
            f"Summarize the loaded documents: {names}",
            title_source=f"Summary: {names}",
        )
        with st.spinner("Summarizing..."):
            summary = summarize_documents(st.session_state.doc_text)
        remember("assistant", summary)

    if st.button("Clear documents", use_container_width=True):
        st.session_state.vectorstore = None
        st.session_state.doc_names = []
        st.session_state.doc_text = ""
        st.rerun()

    st.divider()
    st.header("Chats")

    if st.button("➕ New chat", use_container_width=True):
        start_new_chat()
        st.rerun()

    try:
        conversations = chat_history.list_conversations(user["id"])
    except Exception as e:
        conversations = []
        st.error(f"Could not load your chats: {e}")

    if not conversations:
        st.caption("Your saved chats will appear here.")

    for conversation in conversations:
        is_open = conversation["id"] == st.session_state.conversation_id
        if st.button(
            conversation["title"] or "Untitled chat",
            key=f"conversation_{conversation['id']}",
            use_container_width=True,
            type="primary" if is_open else "secondary",
        ):
            st.session_state.conversation_id = conversation["id"]
            st.session_state.messages = chat_history.get_messages(
                conversation["id"], user["id"]
            )
            st.rerun()

    if st.session_state.conversation_id is not None:
        if st.button("🗑️ Delete this chat", use_container_width=True):
            chat_history.delete_conversation(
                st.session_state.conversation_id, user["id"]
            )
            start_new_chat()
            st.rerun()

st.title("What do you want to ask today?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(CHAT_INPUT_PLACEHOLDER):
    is_new_chat = st.session_state.conversation_id is None
    with st.chat_message("user"):
        st.markdown(prompt)
    remember("user", prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_ai_response(
                prompt, vectorstore=st.session_state.vectorstore
            )
        st.markdown(answer)
    remember("assistant", answer)

    # The sidebar was drawn before this chat existed; redraw it so the new
    # chat shows up in the list right away.
    if is_new_chat:
        st.rerun()
