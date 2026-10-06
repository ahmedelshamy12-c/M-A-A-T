# Ma`at

A Streamlit web app that helps people understand Egyptian legal documents —
laws, contracts, court rulings — by uploading a PDF and asking questions about
it. Answers are produced by a retrieval-augmented generation (RAG) pipeline:
the PDF is chunked and indexed with FAISS, the most similar chunks are
retrieved for the question, and Google Gemini writes the answer.

Features: sign-up / log-in with hashed passwords, PDF upload and indexing,
grounded Q&A in Arabic or English with article citations, one-click document
summaries, saved chat history per user, a contact form whose messages admins
can read, and an admin-only user list with masked national IDs.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then fill in GOOGLE_API_KEY
python init_db.py                  # creates data/data_base.db
streamlit run app.py
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
| `EMBEDDING_MODEL` | `gemini-embedding-2` | Embedding model that indexes the uploaded PDFs      |

Both answer and index in Arabic as well as English. If you change
`EMBEDDING_MODEL`, upload the documents again — an index built with one model
cannot be searched with another.

## Admin account

An administrator is seeded from the environment — by `init_db.py`, and also
automatically the first time anyone logs in (so a fresh deployment needs no
manual step):

| Variable         | Meaning                                             |
| ---------------- | --------------------------------------------------- |
| `ADMIN_EMAIL`    | Email of the admin account (created only if missing) |
| `ADMIN_PASSWORD` | Its password, stored as a PBKDF2 hash               |
| `ADMIN_USERNAME` | Username, defaults to `admin`                        |

Running `python init_db.py` again is safe: the admin is only created when no
user with that email exists yet. `python init_db.py --reset` deletes the
database file first (all accounts and their password hashes are lost).

Only admins can open the **View Users** page, which lists accounts with
national IDs masked and the messages sent through **Contact Us**.

## Project layout

```
app.py                  landing page
init_db.py              creates the database (--reset to start over)
pages/                  Streamlit multipage UI: auth, chat, contact_us, view_users
services/db.py          the only place that opens the SQLite database
services/auth_service.py  sign-up / log-in, password hashing, validation
services/session.py     require_login() page guard + logout button
services/chat_history.py   saved conversations, scoped to their owner
services/contact_service.py  stores and lists Contact Us messages
services/documents_service.py  PDF -> chunks -> FAISS index
services/llm_service.py        retrieval + Gemini prompts (answers, summaries)
data/schema.sql         idempotent database schema
```

The database lives at `data/data_base.db` (resolved relative to the code, not
the current directory) and its tables are created automatically on first use.
Point the `EGY_LAW_DB` environment variable somewhere else to use a different
file.

## Deploying to Streamlit Community Cloud

1. Sign in at <https://share.streamlit.io> with the GitHub account that owns
   this repository, then **Create app → Deploy a public app from GitHub**.
2. Repository: this repo, branch `main`, main file `app.py`. Under
   **Advanced settings** pick Python 3.12.
3. In **Secrets**, paste (with your own values):

   ```toml
   GOOGLE_API_KEY = "..."
   ADMIN_EMAIL = "..."
   ADMIN_PASSWORD = "..."
   ```

   Streamlit exposes top-level secrets as environment variables, which is how
   the app reads them.
4. Deploy. The admin account is created the first time anyone logs in.

Community Cloud's disk is temporary: the SQLite database (accounts, saved
chats, contact messages) is wiped whenever the app restarts or is redeployed.
That is fine for a demo; a permanent deployment would need a hosted database.

## Disclaimer

Ma`at provides general information to help you read and understand legal
documents. It is **not legal advice** and it is not a substitute for a
qualified attorney — always consult a licensed lawyer before acting on
anything the app tells you.
