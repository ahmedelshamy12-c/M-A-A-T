# Issues

Goal: finalize Ma`at for the Afro-Asian competition submission.

## #1 [feature] Working chat: PDF upload → retrieval → Gemini answer
- `pages/chat.py` ignores user input; wire it to `services/documents_service.py` + `services/llm_service.py`.
- Sidebar PDF uploader (multi-file) builds a FAISS index kept in `st.session_state`.
- Chat history rendered with `st.chat_message` for the current session (not persisted).
- Embeddings must handle Arabic legal text (current `all-MiniLM-L6-v2` is English-only).
- Migrate off deprecated `google-generativeai` to `google-genai`.
- Status: done (cab3d7e)

## #2 [bug] Auth & security fixes
- Passwords stored/compared in plaintext → hash them.
- Sign-up: no validation; duplicate email/username crashes with `IntegrityError`; age not validated; always shows success.
- `chat.py`, `contact_us.py`, `view_users.py` crash with `AttributeError` if opened before login page.
- No logout.
- `view_users.py` shows every user's SSN to any logged-in user.
- Status: done (cab3d7e)

## #3 [refactor] Repo cleanup
- `requirements.txt` is empty.
- No `.gitignore`; `.env`, `data/data_base.db`, `__pycache__` are staged.
- `data/egy_law_tables.sql` contains `DROP TABLE users` and drifts from the live DB → replace with a clean schema + init script.
- No README.
- Status: done (cab3d7e)

## #4 [docs] Draft competition documentation
- Fill `docs/afro_asian_software_template.md` from the finished code; team details and screenshots left for the user.
- Depends on #1–#3.
- Status: done (cab3d7e) — drafted; screenshots, "Tested?" boxes and instructor notes left for the student

## #5 [feature] Persist chat history (follow-up)
- `Conversations` / `Messages` tables exist but nothing writes to them; chat is per-session only.
- Status: done — saved via `services/chat_history.py`; sidebar lists, reopens, deletes chats

## #6 [feature] Landing page advertises "Document Summarization" (follow-up)
- No dedicated summarize action; users can only ask the chat to summarize. Either add a "Summarize" button on the chat page or reword the landing card.
- Status: done — "Summarize documents" button on the chat page

## #7 [bug] Contact form doesn't send or store anything (follow-up)
- `pages/contact_us.py` only shows a success message.
- Status: done — stored in `contact_messages`, shown to admins on View Users

## #8 [docs] Deploy to Streamlit Community Cloud
- Repo prepared: schema and admin are created automatically; secrets come from Streamlit Cloud secrets (exposed as env vars). Steps in README.
- Needs the user: sign in to share.streamlit.io, create the app, paste secrets.
- Status: open
