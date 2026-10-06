
# Software Project Documentation | توثيق مشروع البرمجيات

<div class="arabic">
قالب توثيق مشاريع البرمجيات — للمسابقة الأفريقية الآسيوية للتكنولوجيا
</div>

---

## 1. Project Overview | نظرة عامة على المشروع

| Field | Value |
|-------|-------|
| **Project Title** | Ma`at |
| **Project Type** | Web App / AI Tool |
| **Description** | An AI-powered web app for helping people understand Egyptian law. The user uploads their own legal PDF — a law, a contract, or a court ruling — and asks questions about it in Arabic or English. A retrieval-augmented generation (RAG) pipeline finds the relevant passages inside that PDF and Google Gemini writes the answer from them. |
| **Target Users** | Law students, Egyptian citizens, researchers, and small legal practices. |
| **Resolution / Platform** | Mobile-responsive website — runs in any web browser on a desktop, a tablet, or a phone. |
| **Date** | 9/8/2026 |

### Tech Stack | Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3 | The entire project — web app, AI pipeline, and database layer — is written in Python. |
| **Framework** | Streamlit | Builds the multi-page website directly from Python, so no separate front-end code has to be written or maintained. |
| **Database** | SQLite | Stores user accounts in a single file, `data/data_base.db`, opened through Python's built-in `sqlite3` module. |
| **AI / LLM** | google-genai | Calls Google Gemini to write each answer (`gemini-2.5-flash`). |
| **Libraries** | langchain-google-genai, langchain-community, langchain-text-splitters, faiss-cpu, pypdf, python-dotenv | Split the document into chunks, embed them, search them, and read the API key from `.env` (details in the Dependencies table below). |

### Dependencies | المكتبات المستخدمة

All versions are pinned exactly as installed from `requirements.txt`.

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.65.0 | Builds the multi-page web interface (landing, log-in, chat, contact, admin) in Python. |
| python-dotenv | 1.2.4 | Loads `GOOGLE_API_KEY` and the optional settings from a `.env` file instead of hard-coding them. |
| pypdf | 6.19.0 | Extracts the text of every page from the uploaded PDF files. |
| langchain-text-splitters | 1.1.3 | `RecursiveCharacterTextSplitter` cuts the PDF text into overlapping chunks of 2000 characters (250-character overlap). |
| langchain-community | 0.4.2 | Supplies the `FAISS` vector store used to search those chunks. |
| langchain-google-genai | 4.4.0 | Connects the Gemini embedding model (`gemini-embedding-2`) to LangChain. |
| faiss-cpu | 1.15.1 | Facebook's vector-search library — the index that finds the chunks closest to a question. |
| google-genai | 2.28.0 | Google's current Gemini SDK — sends the prompt and returns the written answer. |

<!-- Screenshot: Main screen of your project -->

---

## 2. Problem Statement | بيان المشكلة

<div class="arabic">ن كتير من الناس في مصر بتواجه صعوبة كبيرة في فهم النصوص القانونية بسبب تعقيد اللغة وطول المواد.
</div>

### What problem does this project solve? | ما المشكلة التي يحلها هذا المشروع؟

ن كتير من الناس في مصر بتواجه صعوبة كبيرة في فهم النصوص القانونية بسبب تعقيد اللغة وطول المواد.

Egyptian law is written in long, formal, technical Arabic, so a person who is not a lawyer cannot find the one article they need in a hundred-page law or contract. Ma`at lets any user upload the document they actually have and ask a plain question about it, and the answer is taken from that document instead of from the model's memory.

### Why does it matter? | لماذا هذا مهم؟

Not being able to read a contract or a ruling has real consequences: people sign terms they do not understand, miss deadlines, or give up and assume nothing can be done. Most of the people who need to understand these documents the most — students, citizens, small firms — are exactly the people who can least afford a private lawyer. Making a law readable is therefore a question of fairness, not convenience.

### How is it currently solved? | كيف تُحل المشكلة حالياً؟

Today there are only three options, and all of them are weak. The first is reading the raw text: long, dense documents written in legal jargon, with no way to ask "what does this article mean for me?" The second is paying a lawyer, which is simply not affordable for a student or an average citizen. The third is generic AI chatbots, which answer from general training data and are not connected to the user's own document — so they can be confidently wrong about that specific contract or law.

Ma`at takes the second idea — professional help with a real document — and makes a fast, affordable version of it: the user uploads the document they actually hold and questions it in their own words, without the cost of a lawyer.

---

## 3. Technical Architecture | البنية التقنية

<div class="arabic">
هنا تشرح كيف مشروعك مبني من الداخل — هيكل الملفات والتقنيات المستخدمة
</div>

### Project Structure | هيكل المشروع

```
maat/
├── app.py                  # Entry point / landing page
├── init_db.py              # Creates the SQLite database (--reset to start over)
├── requirements.txt        # Pinned Python dependencies
├── README.md               # Setup, models, admin account, project layout
├── CLAUDE.md               # Notes for AI coding assistants working on the repo
├── ISSUES.md               # Work items and their status
├── .env.example            # Template for the API key and the optional settings
├── docs/
│   └── afro_asian_software_template.md   # This competition document
├── pages/                  # Streamlit multi-page user interface
│   ├── auth.py             # Log in / create account
│   ├── chat.py             # PDF upload, indexing, and the Q&A chat
│   ├── contact_us.py       # Contact details and contact form
│   └── view_users.py       # Admin-only list of accounts
├── services/               # All application logic, no UI code
│   ├── db.py               # The only module that opens SQLite; also applies the schema
│   ├── auth_service.py     # Sign-up, log-in, password hashing, validation
│   ├── session.py          # require_login() page guard + log-out button
│   ├── chat_history.py     # Saved conversations and messages, per user
│   ├── contact_service.py  # Stores and lists Contact Us messages
│   ├── documents_service.py # PDF -> text -> chunks -> FAISS index
│   └── llm_service.py      # Retrieval + Gemini prompts + answers and summaries
└── data/
    ├── schema.sql          # Database schema (idempotent)
    └── data_base.db        # The database file (generated, not in version control)
```

### Architecture Diagram | مخطط البنية

```
                     ┌────────────────────────────┐
                     │       Browser              │
                     │   (no front-end code)      │
                     └────────┬───────────────────┘
                              │ clicks / typing
 ┌────────────────────────────▼───────────────────────────────┐
 │  Streamlit pages      app.py + pages/                      │
 │  Landing, Auth, Chat, Contact Us, View Users               │
 │  Session state, held in the Streamlit server's memory:     │
 │    logged_user, messages, vectorstore, doc_text, ...       │
 └────────┬───────────────────┬───────────────────────────────┘
          │ import            │ import
 ┌────────▼───────────────────▼───────────────────────────────┐
 │  services/                                                 │
 │  session.py, auth_service.py, db.py, chat_history.py,      │
 │  contact_service.py, documents_service.py, llm_service.py  │
 └────────┬───────────────────┬───────────────────────────────┘
          │ parameterised SQL │ vectors in / prompts out
 ┌────────▼───────────┐  ┌────▼──────────────────────────────┐
 │  SQLite            │  │  Google Gemini API                │
 │  data/data_base.db │  │  embeddings: gemini-embedding-2   │
 │  users, chats,     │  │  generation: gemini-2.5-flash     │
 │  contact messages  │  │  api key: GOOGLE_API_KEY from .env│
 └────────────────────┘  └───────────────────────────────────┘

 UPLOAD PATH   PDF -> pypdf reads the text -> 2000-char chunks (250 overlap)
               -> the chunk text is sent to the Gemini embeddings API
               -> the FAISS index is held in the Streamlit server's memory
                  for this session and is lost when the session ends; the
                  uploaded PDF files themselves are never written to disk

 ASK PATH      question -> FAISS similarity search, top 3 chunks
               -> the excerpts + the question are sent to Gemini, which
                  writes the answer (cites article numbers, replies in the
                  language of the question) -> shown in the chat
               -> if nothing is retrieved, or no PDF is loaded, Gemini is
                  asked to answer from general knowledge and to say that
                  the answer is not from the documents
```

### Key Files | الملفات الرئيسية

| File | Purpose | Lines of Code |
|------|---------|:-------------:|
| app.py | Landing page: title, subtitle, disclaimer, the two-column overview, and the button that opens the Auth page. | 63 |
| pages/auth.py | Log-in and create-account tabs; the only page a signed-out visitor can fully use. | 72 |
| pages/chat.py | Sidebar PDF uploader, loaded-document list, Summarize button, saved-chat list (open, new, delete), question box; calls the AI and chat-history services. | 188 |
| pages/contact_us.py | Contact information (email, phone, address) and a name/email/message form that saves the message for the admins. | 36 |
| pages/view_users.py | Admin-only page with two tabs: account cards with masked national IDs, and the Contact Us messages. | 81 |
| services/auth_service.py | Sign-up validation, PBKDF2-SHA256 password hashing, log-in check, admin account from environment variables; no Streamlit import, so it can be tested without a UI. | 219 |
| services/db.py | The single place that opens SQLite (row factory, foreign keys on, path from `EGY_LAW_DB` or `data/`) and applies the schema automatically on first use. | 61 |
| services/documents_service.py | Uploaded PDFs -> text -> overlapping chunks -> FAISS vector store. | 73 |
| services/llm_service.py | Top-3 retrieval, the Gemini prompts (with context / without context / summary), and the answer or the `"Error: ..."` string. | 154 |
| services/session.py | `require_login()` page guard, the admin check, the log-out button, and session cleanup on log-out. | 53 |
| services/chat_history.py | Creates, lists, loads and deletes a user's saved conversations; every query checks the owner. | 119 |
| services/contact_service.py | Validates and stores Contact Us messages, and lists them for admins. | 55 |
| init_db.py | Creates `data/data_base.db` from the schema (optionally from scratch with `--reset`) and seeds the admin account from `ADMIN_EMAIL` / `ADMIN_PASSWORD`. | 62 |
| data/schema.sql | The `users`, `Conversations`, `Messages`, and `contact_messages` tables. | 47 |

---

## 4. Features & User Flow | الميزات وتدفق المستخدم

<div class="arabic">

</div>

### Feature List | قائمة الميزات

| # | Feature | Description | Status |
|---|---------|-------------|:------:|
| 1 | Register an account | The create-account tab asks for username, email, national ID (14 digits), password, job, and age (18–120). Every field is validated before the account is written, and duplicate username / email / national ID are reported as readable messages instead of crashing. | ✅ |
| 2 | Password hashing | Passwords are never stored. Each one is hashed with PBKDF2-HMAC-SHA256 using 600,000 iterations and a random 16-byte salt, and compared with a constant-time check. | ✅ |
| 3 | Log in and log out | Log-in takes email + password and returns the account (id, username, email, role) into the session. The sidebar log-out button clears the user, the chat, and the document index, then returns to the landing page. | ✅ |
| 4 | Page protection | Every protected page calls one shared guard: signed-out visitors get a warning and a link to the Auth page instead of a broken page. | ✅ |
| 5 | PDF upload and indexing | One or more PDFs are uploaded in the sidebar; pypdf reads the page text, Arabic text stored in visual order is repaired, it is split into 2000-character chunks with 250 characters of overlap, embedded with Gemini in batches that respect the free-tier quota (with a progress bar), and indexed with FAISS. The index is held in the Streamlit **server's** memory for that user's session and is lost when the session ends; the PDF files themselves are never written to disk. | ✅ |
| 6 | Grounded Q&A with article citations | The three chunks most similar to the question are sent to Gemini with a prompt that allows only those excerpts, asks it to cite article numbers, to say so plainly when the excerpts do not answer the question, and to reply in the same language as the question (Arabic in, Arabic out). | ✅ |
| 7 | General-knowledge fallback | With no document loaded, or no matching chunk, the assistant answers from its own knowledge and states clearly that the answer is not based on the user's documents. | ✅ |
| 8 | Admin-only user list | Admins see every account newest-first in a three-column card grid (username, email, role, job, age, national ID). The national ID is masked — ten asterisks plus the last four digits. Non-admins are refused. | ✅ |
| 9 | Contact page | Shows the contact email, phone, and address, plus a name/email/message form (pre-filled with the user's name and email). Messages are validated, saved to the database, and shown to admins on the View Users page. | ✅ |
| 10 | Bilingual rendering | Answers keep their Markdown (bold, lists, headings) and a page-level `unicode-bidi: plaintext` stylesheet gives each paragraph the direction of its own content, so Arabic and English both read correctly. | ✅ |
| 11 | Saved chat history | Every question and answer is saved to the `Conversations` and `Messages` tables. The sidebar lists the user's chats (newest first, titled from the first question); a chat can be reopened, a new one started, or the open one deleted. Users only ever see their own chats. The uploaded documents themselves are not saved, so they must be uploaded again in a new session. | ✅ |
| 12 | Document summary | A "Summarize documents" button sends the full text of the loaded PDFs to Gemini and adds a plain-language summary to the chat — key points, rights and obligations, deadlines, penalties, article numbers — written in the documents' language. Very long documents are cut at 300,000 characters and the summary says so. | ✅ |
| 13 | Scanned (image-only) PDFs | Not supported — a PDF with no extractable text returns "No readable text found in these PDFs". There is no OCR step. | ❌ |

> Status: ✅ Complete | ⏳ In Progress | ❌ Not Started

### User Flow | تدفق المستخدم

```
             ┌────────────────────────┐
             │     LANDING PAGE       │
             │       app.py           │
             └────────────┬───────────┘
                          │ "Log in / Create Account"
             ┌────────────▼───────────┐
             │      AUTH PAGE         │
             │    pages/auth.py       │
             └────────────┬───────────┘
                          │ valid credentials
               ┌──────────▼───────────────────────┐
               │          CHAT PAGE               │
               │       pages/chat.py              │
               │  sidebar: upload PDF, index it   │
               │  main: ask, read the answer      │
               └──────┬───────────────────┬───────┘
                      │                   │
           ┌──────────▼─────────────┐  ┌──▼───────────────────────┐
           │   CONTACT US PAGE      │  │    VIEW USERS PAGE       │
           │  pages/contact_us.py   │  │   pages/view_users.py    │
           │  details + a form      │  │   admin only, IDs masked │
           │  (any logged-in user)  │  │   (admins only)          │
           └────────────────────────┘  └──────────────────────────┘

  Streamlit's sidebar lists five entries — the landing page plus Auth,
  Chat, Contact Us and View Users — so the user can move between them at
  any time.

  Guard rails:
   - a protected page opened without logging in  ->  "You must be logged in
     to view this page." plus a link back to the Auth page; nothing else
     renders
   - View Users opened by a non-admin            ->  "Admins only."
   - Log out                                     ->  clears the user, the
     chat and the document index, then returns to the landing page
```

### Screen Reference | دليل الشاشات

| Screen | File / Route | Description | Transitions To |
|--------|-------------|-------------|----------------|
| Landing | `app.py` (first page Streamlit shows) | Wide page: the ⚖️ Ma`at title centred in large dark text, a grey subtitle, a blue note that the app gives general information and is not legal advice, then two equal columns — "📄 Document Summarization" and "💬 Ask the Assistant" — and a highlighted "Log in / Create Account" button. | Auth (via the button); the sidebar also links to the other pages |
| Auth | `pages/auth.py` | Two tabs. **Log in**: email + password. **Create Account/register**: username, email, national ID (14 digits), password, job, age (18–120). Invalid input is shown as a red message; a new account is confirmed and the user then logs in. If someone is already logged in, the page shows who they are with a "Go to chat" button. | Chat (after a successful log-in), or the landing page |
| Chat | `pages/chat.py` (login required) | Wide layout. **Sidebar**: a "Documents" header, a multi-file PDF uploader with a "Process documents" button, a green "Indexed N document(s)" confirmation or a red error, the list of loaded documents, "Summarize documents" and "Clear documents" buttons, then a "Chats" section with "➕ New chat", the saved chats, and "🗑️ Delete this chat"; the log-out panel sits above them. **Main area**: the heading "What do you want to ask today?", the conversation as chat bubbles with Markdown answers, and the box "Ask a question about your documents...". | Sidebar navigation to Auth, Contact Us, View Users; landing page after log-out |
| Contact Us | `pages/contact_us.py` (login required) | Centred layout: a short invitation, then the contact email, phone number, and Cairo address, then a three-field form (Name, Email, Message) whose Send button saves the message and shows a thank-you, or shows "Please fill out all fields." | Sidebar navigation; admins read the message on View Users |
| View Users | `pages/view_users.py` (admins only) | Wide layout with two tabs. **Users**: account cards, three per row, newest first. Each card shows the username as a heading plus email, role, job, age, and the national ID with only the last four digits visible. **Contact messages**: each message with its date, sender email and account. Non-admin users are stopped with "Admins only." | Sidebar navigation; back to the landing page after log-out |

---

## 5. UI/UX Design | تصميم واجهة المستخدم

<div class="arabic">
هنا تحط لقطات الشاشة + وصف التصميم البصري لمشروعك
</div>

### Screenshots | لقطات الشاشة

<!-- Screenshot: Landing page -->
**Landing Page**: One wide page, read from top to bottom: the scales emoji ⚖️ and "Ma`at" in large dark blue-grey letters centred on the screen, a grey subtitle line under it ("Smart System for Assisting with Understanding Egyptian Legal Documents"), a blue information box repeating that the assistant gives general information and is not a replacement for a qualified attorney, then two equal columns side by side — "📄 Document Summarization" on the left, "💬 Ask the Assistant" on the right — a horizontal divider, and one highlighted "Log in / Create Account" button as the single call to action.

<!-- Screenshot: Main dashboard -->
**Dashboard (Chat page)**: A wide screen split into a narrow sidebar and a large conversation area. The sidebar reads "Documents", contains the "Upload PDF documents" box and a full-width "Process documents" button, then either a green "Indexed 2 document(s)." confirmation or a red error message, then a "Loaded documents" list of file names (or the caption "No documents loaded — answers will use general knowledge."), the "Summarize documents" and "Clear documents" buttons, a divider, and the "Chats" section listing the user's saved chats with "➕ New chat" and "🗑️ Delete this chat". Above them sits the shared panel showing who is logged in and the "Log out" button. The main area is headed "What do you want to ask today?", shows the earlier questions and answers as chat bubbles with Markdown formatting, and ends with the input box "Ask a question about your documents...". Arabic answers are laid out right-to-left, English answers left-to-right.

<!-- Screenshot: Key feature screen -->
**Key Feature (a question being answered)**: The chat area a moment after a question has been sent — the user's question in its own bubble, then Gemini's reply in the assistant's bubble below it. The reply is Markdown, so it can carry bold lead-ins and bullet lists, it quotes the wording and the article numbers taken from the uploaded document, is written in the same language as the question, and finishes with a one-line reminder that this is general information and not legal advice. While the model is working, a "Thinking..." spinner occupies the assistant bubble.

<!-- Screenshot: Log-in and sign-up page -->
**Auth Page**: A single screen headed "🔐Enter Gate" with two tabs. The open "Log in" tab holds two stacked boxes — Email and a masked Password — and a full-width "Login" button; a red "Invalid login credentials." message appears under it when the details are wrong. The "Create Account/register" tab holds a two-column form: username, email, and a 14-digit national ID on the left; a masked password, a job field, and an age selector restricted to 18–120 on the right; then a full-width "Create Account" button.

<!-- Screenshot: Admin user list -->
**View Users Page (admin)**: A wide grid of user cards, three across. Each card starts with the username as a heading and lists "Email:", "Role:", "Job:", "Age:", and "National ID:" — where the national ID is shown as ten asterisks followed by the last four digits (for example `**********1234`), so an administrator can identify an account without reading the full ID.

<!-- Add more screenshots as needed -->

### Design System | نظام التصميم

The interface is deliberately plain: almost all of it is Streamlit's own widgets in its default theme, and the only custom styling is a few lines of CSS on the landing page.

| Element | Style |
|---------|-------|
| **Primary Color** | `#2c3e50` (dark blue-grey) — used for the ⚖️ Ma`at title on the landing page |
| **Secondary Color** | `#7f8c8d` (grey) — used for the subtitle under the title |
| **Font** | Streamlit's built-in font in its default theme; no custom web font is loaded, so headings and body text use the standard system sans-serif |
| **Button Style** | Streamlit's flat default buttons; the landing-page call to action and the form submit buttons use the highlighted **primary** style, other buttons the plain style. Rounded corners come from the theme, not from custom CSS. |
| **Layout** | Streamlit's built-in sidebar navigation with five entries — the landing page plus Auth, Chat, Contact Us and View Users. The landing page is a centred title above two equal columns; the Chat page adds its own "Documents" sidebar panel next to the navigation; the Contact Us page uses the narrow **centered** layout; everything else uses **wide**. |
| **Status Feedback** | Streamlit's standard messages throughout: blue `st.info` for the landing disclaimer, green `st.success` for "Indexed N document(s).", "Login successful!" and the contact thank-you, red `st.error` for failed log-in, empty fields and unreadable PDFs, and yellow `st.warning` for the not-logged-in guard |

### Responsive Design | التصميم المتجاوب

There is no custom CSS breakpoint in the project — responsiveness comes from Streamlit's own layout engine, which reflows the page to the browser width.

| Breakpoint | Layout | Tested? |
|------------|--------|:-------:|
| Desktop (1024px+) | Streamlit's **wide** layout on the landing, Chat and View Users pages: the landing page's two columns sit side by side, and View Users shows three user cards per row. On the Chat page the "Documents" sidebar sits next to the conversation. | ☐ |
| Tablet (768-1024px) | Same page, narrower: the columns and cards shrink to the available width and stay side by side. The sidebar can be collapsed with Streamlit's sidebar control to give the content the full width. | ☐ |
| Mobile (< 768px) | Streamlit stacks the columns and cards vertically — one column per block and one user card per row — and the navigation and document panels collapse behind their menu buttons. | ☐ |

---

## 6. Data Sources | مصادر البيانات

<div class="arabic">
هنا تكتب منين جبت الداتا — قاعدة بيانات، API، ملفات، أو داتا مكتوبة في الكود
</div>

### Data Sources | مصادر البيانات

| Source | Type | Description |
|--------|------|-------------|
| Uploaded PDF files | User Input | The laws, contracts, and court rulings the user uploads on the Chat page. Their text is read with pypdf and cut into 2000-character chunks; **the chunk text is sent to Google's Gemini API** to be embedded, and the three retrieved excerpts are sent with every question, so the content of the uploaded documents leaves the app and is processed by an external service. The FAISS index is held in the Streamlit server's memory for the session; the PDF files themselves are never written to the server's disk. |
| Sign-up form | User Input | Username, email, password, national ID, job, and age, typed on the Auth page and validated (unique username / email / national ID, 14-digit ID, password of at least 8 characters, age 18–120) before the account is created. |
| Google Gemini — generation | API | `gemini-2.5-flash` writes each answer from the retrieved excerpts, or from general knowledge when there is nothing to retrieve. Authenticated with `GOOGLE_API_KEY` from `.env`. |
| Google Gemini — embeddings | API | `gemini-embedding-2` converts each document chunk into a vector so FAISS can search it. |
| SQLite database file | Database | `data/data_base.db`, created by `python init_db.py` from `data/schema.sql`. Holds user accounts, saved chats and contact messages. The app creates the tables itself on first use (so a fresh deployment works without running `init_db.py`); its location can be moved with the `EGY_LAW_DB` environment variable. |
| Text written in the code | Static | The assistant's identity, its rules, and its prompt templates (answer with documents, answer without documents, summary) live in `services/llm_service.py`; the interface wording lives in the page files; `.env` supplies the API key and the admin credentials. |

### Database Schema | مخطط قاعدة البيانات

Schema from `data/schema.sql`. Every statement uses `CREATE TABLE IF NOT EXISTS`, so running `python init_db.py` again is safe.

| Table | Columns | Description |
|-------|---------|-------------|
| `users` | `id` (primary key), `username` (unique, required), `email` (unique, required), `password` (PBKDF2-SHA256 hash, required), `job`, `age`, `ssn` (unique, 14-digit Egyptian national ID), `role` (`user` or `admin`, default `user`), `created_at` | One row per account. Written by sign-up and by the admin seeding in `init_db.py`, read by log-in, and listed by the admin page. Passwords are stored only as hashes. |
| `Conversations` | `id` (primary key), `user_id` (foreign key → `users.id`), `title`, `created_at` | One row per saved chat, titled from its first question. Every read and delete checks that the chat belongs to the logged-in user. |
| `Messages` | `id` (primary key), `conversation_id` (foreign key → `Conversations.id`), `sender`, `message`, `created_at` | One row per question, answer, or summary; `sender` is `user` or `assistant`. |
| `contact_messages` | `id` (primary key), `user_id` (foreign key → `users.id`, set to empty if the account is deleted), `name`, `email`, `message`, `created_at` | One row per Contact Us message, shown to admins on the View Users page. |

### External APIs (if any) | واجهات برمجة التطبيقات

| API | Purpose | Rate Limit |
|-----|---------|------------|
| Google Gemini — text generation (`gemini-2.5-flash`) | Writes each answer, using the three excerpts retrieved from the user's PDF; falls back to general knowledge when nothing is retrieved. | Depends on the Google AI Studio plan (free tier is limited) |
| Google Gemini — embeddings (`gemini-embedding-2`) | Turns each document chunk into a vector when a PDF is uploaded, so FAISS can search it. | Depends on the Google AI Studio plan (free tier is limited) |

Both models are read from `.env` (`GEMINI_MODEL`, `EMBEDDING_MODEL`), so they can be changed without editing any code.

---

## 7. Educational Content | المحتوى التعليمي

<div class="arabic">
هنا تكتب المحتوى التعليمي — ماذا يتعلم الطالب من هذا المشروع؟ كيف يتعلق بالمنهج؟
</div>

### Learning Objectives | أهداف التعلم

By the end of this project, the student will be able to:

1. Build a **retrieval-augmented generation (RAG)** pipeline end to end: read a document, split it, index it, retrieve the relevant parts for a question, and prompt a language model to answer only from those parts.
2. Explain **text embeddings and vector search** — what an embedding is, why FAISS finds chunks by meaning rather than by keyword (which matters for Arabic, where the same idea is often written in different words), and why chunks of 1000 characters with 200 characters of overlap retrieve better than whole pages.
3. **Design prompts for reliability**: separate prompts for "answer only from these excerpts" and "answer from general knowledge", instruct the model to cite article numbers, to reply in the same language as the question, and to admit when the documents do not contain the answer instead of inventing one.
4. **Store passwords safely** — PBKDF2-HMAC-SHA256 with 600,000 iterations, a random per-user salt, constant-time comparison, and never keeping plaintext; plus input validation that turns database errors into messages a user can act on.
5. **Design and query a relational database in SQLite** — primary keys, unique constraints, foreign keys, the `role` check constraint, and why every query uses parameter placeholders instead of string concatenation.
6. **Build a multi-page web application in Streamlit**, including `st.session_state` for per-user state and a single shared `require_login()` guard so that "not logged in" and "admins only" are handled in one place for every page.
7. **Separate the interface from the logic** — pages contain UI only, services contain the business logic, so the logic can be exercised without a browser.

### Cultural / Historical Context | السياق الثقافي / التاريخي

| Topic | Description |
|-------|-------------|
| The name "Ma`at" | Ma`at (also written Ma'at) is the ancient Egyptian idea of truth, justice, and the order that keeps the world and society together, traditionally shown as a woman holding the scales of justice — the ⚖️ emoji in the app's title. The project takes the name because it is about the same thing: making the law fair to read, so that a person can weigh what a document says instead of taking it on trust. |
| Access to law in Egypt | Egyptian law is published in long, formal Arabic, and a contract or a ruling is often hundreds of pages long, so understanding it normally means paying for a lawyer or giving up. Ma`at lets a law student, a citizen, or a small firm upload the actual document and ask a plain question in Arabic or English — bringing the law closer to the people it applies to, in both languages. |

### Curriculum Alignment | التوافق مع المنهج

| Skill Area | What the Student Practices |
|------------|---------------------------|
| Problem Solving | Turning a real, everyday problem — legal texts that people cannot read — into concrete working steps: upload, parse, chunk, embed, index, retrieve, answer, and handle the case where there is nothing to retrieve. |
| Computational Thinking | Abstraction (breaking the PDF-to-answer job into small functions in `services/`), data modelling (a `users` table with constraints and two roles), and algorithm design (similarity search with k = 3 and overlapping chunks). |
| Creativity | Interface design in Streamlit: a bilingual page, Markdown answers that flow right-to-left in Arabic and left-to-right in English, and a two-column landing page that explains the product in one screen. |
| Collaboration | Working with external services and open-source libraries on someone else's terms — the Gemini API, FAISS, and LangChain — and documenting the result so that anyone else can install it and run it. |
| Technical Writing | `README.md`, docstrings that explain *why* each module exists, a commented and idempotent database schema, and this bilingual English/Arabic competition document. |

---

## 8. Marketing Plan | خطة تسويقية

> **Short version** — for full marketing plans, use the main Afro-Asian template.

<div class="arabic">Short marketing plan: target law students, Egyptian citizens, researchers, and small legal practitioners; promote the website through social media, WhatsApp, university groups, and legal communities; share demo videos, simple legal explainers, FAQs, and screenshots to show how the app makes Egyptian law easier to understand, while building trust and increasing visits and engagement.


</div>

### Target Audience | الجمهور المستهدف

- **Primary**: Law students and Egyptian citizens who have to read a law, a contract, or a ruling in Arabic and cannot afford a private lawyer.
- **Secondary**: Researchers, and small legal practices handling case files without a large legal team.
- **Tertiary**: Legal communities, university student groups, and coding communities interested in Arabic-language AI tools.

### Platforms | المنصات

- Web browser on a desktop or laptop (Chrome, Firefox, Edge) — the app is a website, so no installation is needed for the user.
- Mobile phone browser — the Streamlit layout adapts to a narrow screen.
- University and lab computers — the app can also be run locally with Python and a `.env` file for a demo.

### Promotion Ideas | أفكار ترويجية

1. Share a short demo video — upload a real contract, ask one question, get an answer that cites the article — on YouTube and TikTok.
2. Post screenshots and short legal explainers in university groups on WhatsApp and social media, and share them inside law-student groups.
3. Publish simple legal explainers and an FAQ showing that the same question gets an Arabic answer or an English answer, and that the assistant says when a document does not contain the answer.
4. Present the app inside legal communities and Arabic-language AI / open-source communities, sharing the repository so other students can run it.
5. Submit and demonstrate it at the Afro-Asian Tech Forum competition.

---

## 9. Student Worksheet | ورقة عمل الطالب

> **Instructions**: Copy this section into your own document and fill it in for YOUR project.

---

### My Project Information | معلومات مشروعي

**Student Name**: ________Ahmed Medhat Elshamy___________________

**Project Title**: __________maat_________________

**Date**: __________!19,8 _________________

---

#### What is your project about? | عن ماذا يتحدث مشروعي؟

_______________________________________________
___________egyption law____________________________________

#### What problem does it solve? | ما المشكلة التي يحلها؟

_______________________________________________
___________difculty of anderstanding egyption law
---

### My Tech Stack | التقنيات المستخدمة

**My project type** (circle one): Web App / Desktop App / Mobile App / Python Script / Other: _______

**Technologies I used**:

| Category | Technology |
|----------|-----------|
| Language | Python 3 |
| Framework | Streamlit 1.65.0 |
| Database | SQLite (data/data_base.db) |
| Libraries | pypdf, langchain-text-splitters, langchain-community (FAISS), langchain-google-genai, google-genai, python-dotenv |

---

### My Screens | شاشات مشروعي

Draw or describe all the screens in your project:

| Screen Name | What the user sees/does | How to get here |
|-------------|------------------------|-----------------|
| Landing | The ⚖️ Ma`at title, the subtitle, the disclaimer, the two columns, and the "Log in / Create Account" button. | Open `app.py` with `streamlit run app.py` |
| Auth — Log in | Email and password boxes and a Login button; a red message if the details are wrong. | The landing page button, or the sidebar |
| Auth — Create Account | Username, email, 14-digit national ID, password, job and age (18–120), and a Create Account button. | The landing page button, or the sidebar |
| Chat | Sidebar with the PDF uploader, the loaded-document list, the Summarize button and the saved chats; main area with the conversation and the question box. | Automatically after logging in |
| Contact Us | Contact email, phone, address, and a name / email / message form. | Sidebar, while logged in |
| View Users | Cards of every account, three per row, with the national ID masked, plus a tab with the Contact Us messages. | Sidebar, while logged in as an admin |

---

### My Features | ميزات مشروعي

| Feature | What it does | Status |
|---------|-------------|:------:|
| Register an account | Checks username, email, 14-digit national ID, password, job and age, then saves the account with the password as a PBKDF2 hash. | ✅ |
| Log in and log out | Checks email + password; logging out clears the user, the chat, and the document index. | ✅ |
| Page protection | Protected pages stop and offer a link to the log-in page; View Users is admins only. | ✅ |
| PDF upload and indexing | Uploads one or more PDFs, reads the text, cuts it into chunks, and builds a FAISS index with Gemini embeddings. | ✅ |
| Grounded Q&A | Sends the 3 most similar chunks to Gemini, which answers only from them, cites article numbers, and replies in the language of the question. | ✅ |
| General-knowledge fallback | With no document, or no matching text, Gemini answers from general knowledge and says the answer is not from the documents. | ✅ |
| Admin user list | Admins see all accounts with the national ID masked; other users are refused. | ✅ |
| Contact form | A name / email / message form; messages are saved and admins read them on View Users. | ✅ |
| Document summary | One button gives a plain-language summary of the uploaded PDFs in their own language. | ✅ |
| Saved chat history | Every chat is saved; the sidebar lists past chats to reopen or delete. | ✅ |

---

### My Data | بيانات مشروعي

**Where does data come from?**

_egyption law documents______________________________________________

**What data is stored?**

_______fiass file________________________________________

---

### What I Learned | ما تعلمته

1. The hardest part of building my project was: _____rag____________________________

2. The most fun part of building my project was: ____frontend_____________________________

3. If I had more time, I would add: _______________real robots__________________

4. One thing I would do differently: __________no thing_______________________

---

### Screenshot of My Project | لقطة شاشة من مشروعي

<!-- Paste a screenshot of your project running here -->

---

**Instructor Notes** | ملاحظات المدرس:

_______________________________________________
_______________________________________________

---

<div class="session-footer">
  <p>Techno Kids, Techno Future — Software Documentation Template</p>
  <p>Afro-Asian Tech Forum · Software Category · 2026</p>
</div>
