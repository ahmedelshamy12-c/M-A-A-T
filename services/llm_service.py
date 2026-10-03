"""Answer a question with Gemini, grounded in the user's documents.

`get_ai_response` retrieves the closest chunks from the session's FAISS index
and asks Gemini to answer from them; with no index (or no matching chunk) it
falls back to general knowledge and says so. Like the rest of the services it
never raises: failures come back as `"Error: ..."` strings for the page to show.

Prompts are bilingual by design: the answers follow the language of the
question, because the documents and the users are Arabic.
"""

import os

import streamlit as st
from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"
SEARCH_RESULTS = 3

ROLE = (
    "You are Ma`at, an assistant that helps people understand Egyptian law: "
    "laws, contracts and court rulings."
)

COMMON_RULES = f"""{ROLE}

Rules:
- Reply in the SAME language as the user's question: an Arabic question gets an
  Arabic answer, an English question an English answer.
- Be clear and concise, and quote the legal text when the exact wording matters.
- Finish with a one-line reminder that this is general information meant to help
  the user understand the law, not legal advice.
"""

CONTEXT_PROMPT = f"""{COMMON_RULES}
- Answer using ONLY the excerpts below. Anything you know that they contradict
  is out of date for this question: ignore it.
- Cite the article numbers when the excerpts give them.
- If the excerpts do not contain the answer, say so plainly instead of inventing
  an answer.

Excerpts from the user's documents:
---
{{context}}
---

User question:
{{user_question}}
"""

NO_CONTEXT_PROMPT = f"""{COMMON_RULES}
- Answer from your own general knowledge of Egyptian law.
- State clearly that the answer is NOT based on the user's documents: either no
  documents were uploaded, or none of them cover this question.
- Say so when you are unsure rather than guessing.

User question:
{{user_question}}
"""


def get_ai_response(
    user_question: str, *, vectorstore=None, model_name: str = None
) -> str:
    """Answer `user_question`, preferring `vectorstore` for the facts.

    Falls back to `st.session_state["vectorstore"]` when no vector store is
    passed. Returns the answer, or an `"Error: ..."` string.
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            return "Error: GOOGLE_API_KEY was not found in the environment variables"

        model_name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

        vs = vectorstore
        if vs is None:
            vs = st.session_state.get("vectorstore")

        excerpts = []
        if vs:
            for doc in vs.similarity_search(user_question, k=SEARCH_RESULTS):
                page_content = getattr(doc, "page_content", "") or ""
                if page_content.strip():
                    excerpts.append(page_content)

        if excerpts:
            prompt = CONTEXT_PROMPT.format(
                context="\n\n".join(excerpts), user_question=user_question
            )
        else:
            prompt = NO_CONTEXT_PROMPT.format(user_question=user_question)

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name, contents=prompt
        )
        return getattr(response, "text", "") or ""

    except Exception as e:
        return f"Error: {str(e)}"