# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Ma`at** — a Streamlit web app that helps users understand Egyptian legal documents (laws, contracts, rulings) via RAG over uploaded PDFs, answered by Google Gemini. Built for the Afro-Asian technology competition; `docs/afro_asian_software_template.md` is the bilingual EN/AR competition documentation. Work items are tracked in `ISSUES.md`.

## Commands

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env              # GOOGLE_API_KEY, optional ADMIN_*, GEMINI_MODEL, EMBEDDING_MODEL
.venv/bin/python init_db.py       # create data/data_base.db (+ admin from ADMIN_EMAIL/ADMIN_PASSWORD); --reset wipes it
.venv/bin/streamlit run app.py
```

There is no test suite or linter. Verification is done with `py_compile` plus Streamlit `AppTest` scripts. Gotchas:
- Run pages through the entrypoint: `AppTest.from_file("<abs path>/app.py").run()` then `at.switch_page("pages/chat.py").run()`. Running a page file directly as the entrypoint breaks `st.page_link("pages/auth.py")`.
- Point tests at a throwaway DB with `EGY_LAW_DB=/path/to/test.db` and run with `PYTHONPATH=.` — never test against `data/data_base.db`.
- Mock Gemini by patching `google.genai.Client`; give the page a fake vectorstore (any object with `similarity_search(q, k)`).

## Architecture

Streamlit multipage app (v1 `pages/` directory): `app.py` is the landing page, pages navigate with `st.switch_page("pages/<name>.py")`. Logic lives in `services/`.

- **DB**: `services/db.py` is the only place that opens SQLite (`get_connection()` → `sqlite3.Row` rows, foreign keys on; path resolved from the file, overridable via `EGY_LAW_DB`). Schema in `data/schema.sql` (idempotent) is applied automatically on a process's first connection to a DB file, and by `init_db.py`. Tables: `users`, `Conversations`, `Messages`, `contact_messages`. The DB file and `.env` are git-ignored. `services/__init__.py` loads `.env`, because Streamlit runs each page file on its own (a visitor may never hit `app.py`).
- **Auth**: `services/auth_service.py` (no Streamlit import) — PBKDF2-SHA256 hashing, `register()` raises `ValueError` with user-facing messages, `login()` returns `{"id","username","email","role"}` or `None`. That dict lives in `st.session_state.logged_user`. Roles are `user`/`admin`; the admin comes from `ADMIN_EMAIL`/`ADMIN_PASSWORD` via `ensure_env_admin()`, run by `init_db.py` and once per process on first `login()` (so cloud deploys need no manual step).
- **Page guard**: protected pages call `services/session.require_login(admin=False)` near the top; it stops the render for anonymous/non-admin users and draws the sidebar logout button (logout also clears the chat/document session keys listed in `VOLATILE_KEYS`). `view_users.py` is admin-only: user cards with masked national IDs + a Contact messages tab (`services/contact_service.py`).
- **RAG chat** (`pages/chat.py`): sidebar PDF upload → `documents_service.get_pdf_text()` + `index_text()` (2000/250 chunks → FAISS with Gemini embeddings, `gemini-embedding-2` default, embedded in batches of 50 that sleep and retry on 429 — the free tier allows only 100 chunks/minute). `fix_visual_arabic()` repairs PDFs whose Arabic pypdf returns as presentation-form glyphs in reversed word order; the index and raw text live in `st.session_state.vectorstore` / `doc_text`. "Summarize documents" sends the full text (capped at 300k chars) to `llm_service.summarize_documents()`. Questions go to `llm_service.get_ai_response()` (top-3 retrieval, `google-genai` client, `gemini-2.5-flash` default) which returns `"Error: ..."` strings instead of raising, answers in the question's language, and falls back to general knowledge when nothing is retrieved. Every message goes through `remember()` in `chat.py`, which saves it via `services/chat_history.py` (all functions take `user_id` and enforce ownership); the sidebar lists, reopens and deletes saved chats. Documents are not persisted. Arabic direction is handled with a page-level `unicode-bidi: plaintext` stylesheet so Markdown is still rendered.
- `google-generativeai` (deprecated) and HuggingFace embeddings were removed; don't reintroduce them.

## Conventions

All text files use LF line endings, enforced by `.gitattributes`.

## Workflow

Track work in `ISSUES.md`. In this repo Claude implements changes directly — do not delegate to OpenCode (user's instruction, overrides the global delegate workflow).
