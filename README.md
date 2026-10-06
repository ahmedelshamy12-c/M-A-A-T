# Ma`at ⚖️

A simple website that helps people understand Egyptian legal documents.
Upload a PDF (a law, a contract or a court ruling), then ask questions about
it in Arabic or English — type your own or click a suggested question — or
get a short summary. Google Gemini writes the
answers.

The code is kept on purpose very simple: plain variables, plain functions and
only three libraries, so a beginner can read all of it.

## How it works (simple RAG)

1. The PDF text is cut into parts of 2000 characters.
2. Gemini turns every part into a list of numbers (an *embedding*).
3. Your question is turned into numbers too, and every part gets a score:
   multiply the two lists number by number and add everything up.
4. The 5 parts with the highest score are sent to Gemini with your question.

## Run it on your computer

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# open .streamlit/secrets.toml and paste your Gemini API key

streamlit run app.py               # run it from this folder
```

Get a free Gemini API key at <https://aistudio.google.com/apikey>.
The database (`data/data_base.db`) is created automatically.
**The first person who signs up becomes the admin.**

## Put it online (Streamlit Community Cloud)

1. Go to <https://share.streamlit.io> and sign in with GitHub.
2. Create app → pick this repository, branch `main`, file `app.py`.
3. In **Advanced settings → Secrets** paste: `GOOGLE_API_KEY = "your-key"`.
4. Deploy. Sign up first so that you become the admin.

The cloud disk is temporary: users and chats are deleted when the app restarts.

## Files

```
app.py          start of the app: makes the tables, builds the menu
services/       small functions, one file per topic:
  database.py        open the database, create the tables
  user_service.py    sign up, log in, list users
  chat_service.py    save and load chats
  contact_service.py save and list contact messages
  pdf_service.py     read the PDF, cut it into parts
  ai_service.py      Gemini: embeddings, best parts, answers, summaries
app_pages/      the screens: home, login, chat, contact, admin, logout
data/schema.sql the database tables
```

## Limits

- Passwords are saved as plain text — this is a learning project.
- PDFs bigger than 90 parts (about 180,000 characters) are refused, because
  the free Gemini plan only allows about 100 embeddings per minute.
- There is no error handling: if Gemini's free quota runs out, the page shows
  an error. Wait a minute (or until tomorrow for the daily limit) and try again.
- Scanned PDFs (pictures of text) can't be read, and some Arabic PDFs come out
  with their words in reverse order.

## Disclaimer

Ma`at gives general information to help you understand legal documents. It is
**not legal advice**. Always ask a qualified lawyer before acting on it.
