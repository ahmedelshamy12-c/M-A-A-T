"""Answer a question with Gemini, grounded in the user's documents.

`get_ai_response` retrieves the closest chunks from the session's FAISS index
and asks Gemini to answer from them; with no index (or no matching chunk) it
falls back to general knowledge and says so. `summarize_documents` sends the
full document text for a plain-language summary. Like the rest of the services it
never raises: failures come back as `"Error: ..."` strings for the page to show.

Prompts are bilingual by design: the answers follow the language of the
question, because the documents and the users are Arabic.
"""

import os
import re

import streamlit as st
from google import genai

from services.documents_service import (
    RATE_LIMIT_MESSAGE,
    is_rate_limit,
    retry_on_rate_limit,
)

DEFAULT_MODEL = "gemini-2.5-flash"
SEARCH_RESULTS = 6
# A user is waiting on the answer, so give up on a rate limit sooner than
# document indexing does.
ANSWER_ATTEMPTS = 3

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

{{language_rule}}

User question:
{{user_question}}
"""

NO_CONTEXT_PROMPT = f"""{COMMON_RULES}
- Answer from your own general knowledge of Egyptian law.
- State clearly that the answer is NOT based on the user's documents: either no
  documents were uploaded, or none of them cover this question.
- Say so when you are unsure rather than guessing.

{{language_rule}}

User question:
{{user_question}}
"""


SUMMARY_MAX_CHARS = 300_000

SUMMARY_PROMPT = f"""{ROLE}

Summarize the legal document(s) below for a reader who is not a lawyer.

Rules:
- Write the summary in the SAME language as the documents (Arabic documents get
  an Arabic summary).
- Start with one sentence saying what kind of document it is and what it is
  about, then list the key points as bullets: parties or who it applies to,
  main rights and obligations, deadlines, amounts, penalties, and anything
  unusual the reader should notice. Cite article numbers when present.
- Use only the text below; do not add outside facts.
- Finish with a one-line reminder that this is general information meant to help
  the user understand the document, not legal advice.
{{truncation_note}}
Documents:
---
{{text}}
---
"""

_ARABIC = re.compile("[\u0600-\u06FF]")


def language_rule(user_question):
    """Name the answer language explicitly.

    "Same language as the question" alone isn't enough: with Arabic excerpts
    in the prompt, Gemini tends to answer English questions in Arabic.
    """
    if _ARABIC.search(user_question or ""):
        return "IMPORTANT: The question is in Arabic. Write the entire answer in Arabic."
    return (
        "IMPORTANT: The question is in English. Write the entire answer in "
        "English, even though the excerpts may be in Arabic (quote Arabic legal "
        "wording only when it helps, with an English translation)."
    )


TRUNCATION_NOTE = (
    "- The documents were too long and were cut off; say that the summary "
    "covers only the first part.\n"
)


def _generate(prompt, model_name=None):
    """Send `prompt` to Gemini and return its text, or an `"Error: ..."` string."""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY was not found in the environment variables"

        model_name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        client = genai.Client(api_key=api_key)
        response = retry_on_rate_limit(
            client.models.generate_content,
            model=model_name,
            contents=prompt,
            attempts=ANSWER_ATTEMPTS,
        )
        return getattr(response, "text", "") or ""
    except Exception as e:
        return _error_text(e)


def _error_text(error):
    if is_rate_limit(error):
        return f"Error: {RATE_LIMIT_MESSAGE}"
    return f"Error: {str(error)}"


def get_ai_response(
    user_question: str, *, vectorstore=None, model_name: str = None
) -> str:
    """Answer `user_question`, preferring `vectorstore` for the facts.

    Falls back to `st.session_state["vectorstore"]` when no vector store is
    passed. Returns the answer, or an `"Error: ..."` string.
    """
    try:
        vs = vectorstore
        if vs is None:
            vs = st.session_state.get("vectorstore")

        excerpts = []
        if vs:
            results = retry_on_rate_limit(
                vs.similarity_search,
                user_question,
                k=SEARCH_RESULTS,
                attempts=ANSWER_ATTEMPTS,
            )
            for doc in results:
                page_content = getattr(doc, "page_content", "") or ""
                if page_content.strip():
                    excerpts.append(page_content)
    except Exception as e:
        return _error_text(e)

    if excerpts:
        prompt = CONTEXT_PROMPT.format(
            context="\n\n".join(excerpts),
            user_question=user_question,
            language_rule=language_rule(user_question),
        )
    else:
        prompt = NO_CONTEXT_PROMPT.format(
            user_question=user_question,
            language_rule=language_rule(user_question),
        )

    return _generate(prompt, model_name)


def summarize_documents(text: str, *, model_name: str = None) -> str:
    """Plain-language summary of the full document text, or `"Error: ..."`.

    The whole text is sent (not retrieved chunks), capped at
    `SUMMARY_MAX_CHARS`; when it is cut, the model is told to say so.
    """
    text = (text or "").strip()
    if not text:
        return "Error: there is no document text to summarize."

    truncated = len(text) > SUMMARY_MAX_CHARS
    prompt = SUMMARY_PROMPT.format(
        text=text[:SUMMARY_MAX_CHARS],
        truncation_note=TRUNCATION_NOTE if truncated else "",
    )
    return _generate(prompt, model_name)
