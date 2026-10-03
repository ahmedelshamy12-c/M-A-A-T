# Ma`at

A Streamlit web app that helps people understand Egyptian legal documents —
laws, contracts, court rulings — by uploading a PDF and asking questions about
it. Answers are produced by a retrieval-augmented generation (RAG) pipeline:
the PDF is chunked and indexed with FAISS, the most similar chunks are
retrieved for the question, and Google Gemini writes the answer.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then fill in GOOGLE_API_KEY
python init_db.py                  # creates data/data_base.db
streamlit run app.py               # run from the repo root
```

If you already have a `data/data_base.db` from an older version (no `role`
column, passwords in plaintext), recreate it with `python init_db.py --reset` —
that deletes the file, so every account has to be created again.

Log in with an account you create on the **Auth** page, or with the admin
account below, then open **Chat** to upload PDFs and ask questions.

## Models

`GOOGLE_API_KEY` is the only required variable; both models can be swapped from
`.env` without touching the code:

| Variable          | Default                | Meaning                                             |
| ----------------- | ---------------------- | --------------------------------------------------- |
| `GEMINI_MODEL`    | `gemini-2.5-flash`     | Gemini model that writes the answers                |
| `EMBEDDING_MODEL` | `gemini-embedding-001` | Embedding model that indexes the uploaded PDFs      |

Both answer and index in Arabic as well as English. If you change
`EMBEDDING_MODEL`, upload the documents again — an index built with one model
cannot be searched with another.

## Admin account

`init_db.py` seeds an administrator from the environment:

| Variable         | Meaning                                             |
| ---------------- | --------------------------------------------------- |
| `ADMIN_EMAIL`    | Email of the admin account (created only if missing) |
| `ADMIN_PASSWORD` | Its password, stored as a PBKDF2 hash               |
| `ADMIN_USERNAME` | Username, defaults to `admin`                        |

Running `python init_db.py` again is safe: the admin is only created when no
user with that email exists yet. `python init_db.py --reset` deletes the
database file first (all accounts and their password hashes are lost).

Only admins can open the **View Users** page, which lists accounts with
national IDs masked.

## Project layout

```
app.py                  landing page
init_db.py              creates the database (--reset to start over)
pages/                  Streamlit multipage UI: auth, chat, contact_us, view_users
services/db.py          the only place that opens the SQLite database
services/auth_service.py  sign-up / log-in, password hashing, validation
services/session.py     require_login() page guard + logout button
services/documents_service.py  PDF -> chunks -> FAISS index
services/llm_service.py        retrieval + Gemini prompt
data/schema.sql         idempotent database schema
```

The database lives at `data/data_base.db` (resolved relative to the repo, so
the app must be started from the repo root). Point the `EGY_LAW_DB`
environment variable somewhere else to use a different file.

## Disclaimer

Ma`at provides general information to help you read and understand legal
documents. It is **not legal advice** and it is not a substitute for a
qualified attorney — always consult a licensed lawyer before acting on
anything the app tells you.
