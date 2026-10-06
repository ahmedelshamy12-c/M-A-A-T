"""Chat page: upload PDFs, ask questions, get answers grounded in them.

Answers are Markdown (bold, lists, headings), so they are rendered with plain
`st.markdown`. Arabic needs no HTML wrapper: a single page-level stylesheet
gives every paragraph the direction of its own content, which is also what
keeps mixed Arabic/English answers readable.
"""

import streamlit as st

from services.documents_service import build_vectorstore
from services.llm_service import get_ai_response
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

require_login()

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
                vectorstore = build_vectorstore(uploaded_files)

            if vectorstore is None:
                st.error(
                    "No readable text found in these PDFs "
                    "(scanned images aren't supported)."
                )
            else:
                st.session_state.vectorstore = vectorstore
                st.session_state.doc_names = [file.name for file in uploaded_files]
                st.success(
                    f"Indexed {len(st.session_state.doc_names)} document(s)."
                )
        except Exception as e:
            st.error(f"Could not process the documents: {str(e)}")

    doc_names = st.session_state.doc_names
    if doc_names:
        st.subheader("Loaded documents")
        for name in doc_names:
            st.markdown(f"- {name}")
    else:
        st.caption("No documents loaded — answers will use general knowledge.")

    st.divider()

    if st.button("Clear documents", use_container_width=True):
        st.session_state.vectorstore = None
        st.session_state.doc_names = []
        st.rerun()

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("What do you want to ask today?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(CHAT_INPUT_PLACEHOLDER):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_ai_response(
                prompt, vectorstore=st.session_state.vectorstore
            )
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})