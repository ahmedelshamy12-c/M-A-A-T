# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Ma`at** — a Streamlit app that helps people understand Egyptian legal documents: upload a PDF, ask questions (Arabic or English), get a summary. Built for the Afro-Asian technology competition; `docs/afro_asian_software_template.md` is the bilingual competition document. Work items are in `ISSUES.md`.

**The code must stay beginner-simple** (the user's explicit requirement: "written by a 12-year-old"): plain variables and plain functions, no classes, no type hints, no try/except, no password hashing, no extra libraries beyond `streamlit`, `pypdf`, `google-genai`. Use simple `if` checks for user-facing validation. Don't reintroduce langchain, FAISS, python-dotenv, or an init script.

## Commands

```bash
.venv/bin/pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # add GOOGLE_API_KEY
.venv/bin/streamlit run app.py    # run from the repo root (DB path is relative)
```

No test suite. Verify with Streamlit `AppTest`: `AppTest.from_file("<abs>/app.py")`, set `at.secrets["GOOGLE_API_KEY"]`, point `services.database.DATABASE_FILE` at a temp file, mock `google.genai.Client`, and use `at.switch_page("app_pages/<page>.py")` — pages only exist in the navigation when the session allows them (e.g. admin.py only for an admin user). Mocks won't catch real-API behavior: always keep the Gemini client in a variable before calling it (a temporary `get_gemini().models...` gets closed mid-request), and `embed_content` is called once per text because some embedding models merge a list into one vector.

## Architecture

- `app.py` creates the tables (`data/schema.sql`) and builds `st.navigation(position="top")` from `st.session_state.user`: logged out → Home, Log in; logged in → Chat (default), Home, Contact us, Log out; admin also gets Admin. Pages live in `app_pages/` (not `pages/`, which would trigger Streamlit's legacy auto-discovery).
- `services/` holds every function, one plain module per topic (no `__init__.py`, no classes): `database.py` (`connect`, `create_tables`), `user_service.py`, `chat_service.py`, `contact_service.py` — SQLite tables `users`, `chats`, `messages`, `contact_messages`; plain-text passwords; first user to sign up gets role `admin` — then `pdf_service.py` and `ai_service.py` for Gemini (`read_pdf`, `split_text` every 2000 chars, `embed` with `gemini-embedding-001`, `find_best_parts` = dot product top 5, `answer_question` / `summarize` with `gemini-2.5-flash`, answer language chosen by whether the question has Arabic letters).
- `app_pages/chat.py`: one PDF at a time; >90 parts is refused (free tier ≈100 embeddings/minute plus a daily cap); parts, vectors and full text live in session state; every message is saved via `save()` into `chats`/`messages`, and the sidebar lists the user's chats. `st.pills` above the chat input offers the fixed English questions from `QUESTION_COLORS` (each shown in its own color via `format_func=colored`, so the value stays the plain question); its `on_change` callback copies the pick into `suggested_question` and resets the pill so it can be clicked again.
- Each protected page starts with the same 3-line `if "user" not in st.session_state` check.
- The API key comes from `st.secrets` (`.streamlit/secrets.toml`, git-ignored; on Streamlit Cloud, the app's Secrets box).

## Workflow

Track work in `ISSUES.md`. In this repo Claude implements changes directly — do not delegate to OpenCode (user's instruction, overrides the global delegate workflow). All text files use LF line endings (`.gitattributes`).
