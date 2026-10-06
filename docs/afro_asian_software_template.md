
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
| **Description** | An AI-powered web app for helping people understand Egyptian law. The user uploads their own legal PDF — a law, a contract, or a court ruling — and asks questions about it in Arabic or English. A very simple retrieval-augmented generation (RAG) design finds the parts of the PDF that match the question, and Google Gemini writes the answer from them. The code is kept deliberately basic — plain variables, plain functions, and only three libraries — so that a beginner can read every line. |
| **Target Users** | Law students, Egyptian citizens, researchers, and small legal practices. |
| **Resolution / Platform** | Mobile-responsive website — runs in any web browser on a desktop, a tablet, or a phone. |
| **Date** | 9/8/2026 |

### Tech Stack | Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3 | The whole project is written in Python. |
| **Framework** | Streamlit | Builds the website directly from Python: pages, buttons, forms, chat bubbles, and the top menu. |
| **Database** | SQLite | Stores users, saved chats, and contact messages in one file, `data/data_base.db`, using Python's built-in `sqlite3` module. |
| **AI** | Google Gemini (`google-genai`) | `gemini-embedding-001` turns text into numbers for searching; `gemini-2.5-flash` writes the answers and summaries. |
| **PDF reading** | pypdf | Reads the text out of the uploaded PDF. |

### Dependencies | المكتبات المستخدمة

Only three libraries are installed (`requirements.txt`); everything else comes with Python.

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.65.0 | The web interface. |
| pypdf | 6.19.0 | Reads the text of every page of the PDF. |
| google-genai | 2.28.0 | Talks to Google Gemini: embeddings for search, and the written answers. |

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
├── app.py              # Start of the app: creates the tables and builds the menu
├── services/           # Small functions, one file per topic
│   ├── database.py         # Opens the database, creates the tables
│   ├── user_service.py     # Sign up, log in, list users
│   ├── chat_service.py     # Save and load chats
│   ├── contact_service.py  # Save and list contact messages
│   ├── pdf_service.py      # Read the PDF, cut it into parts
│   └── ai_service.py       # Gemini: embeddings, best parts, answers, summaries
├── app_pages/
│   ├── home.py         # Welcome page
│   ├── login.py        # Log in / Sign up tabs
│   ├── chat.py         # Upload a PDF, ask questions, summarize, saved chats
│   ├── contact.py      # Contact details and a message form
│   ├── admin.py        # Users and contact messages (admin only)
│   └── logout.py       # Logs the user out
├── data/
│   ├── schema.sql      # The database tables
│   └── data_base.db    # The database file (made automatically, not in git)
├── .streamlit/
│   └── secrets.toml.example  # Where the Gemini API key goes
├── requirements.txt    # The 3 libraries
├── README.md
└── docs/afro_asian_software_template.md   # This document
```

### Architecture Diagram | مخطط البنية

```
 ┌───────────────────────────────────────────┐
 │  Browser                                  │
 └─────────────────────┬─────────────────────┘
                       │
 ┌─────────────────────▼─────────────────────┐
 │  app.py  (menu)  ->  app_pages/*.py       │
 └─────────────────────┬─────────────────────┘
                       │ calls functions in
 ┌─────────────────────▼─────────────────────┐
 │  services/  (database, user, chat,        │
 │            contact, pdf, ai)              │
 └──────────┬──────────────────────┬─────────┘
            │                      │
 ┌──────────▼─────────┐  ┌─────────▼─────────────────┐
 │  SQLite            │  │  Google Gemini            │
 │  data/data_base.db │  │  gemini-embedding-001     │
 │  users, chats,     │  │  gemini-2.5-flash         │
 │  messages, contact │  │                           │
 └────────────────────┘  └───────────────────────────┘

 UPLOAD   PDF -> read the text -> cut it every 2000 characters
          -> (more than 90 parts? refuse the file)
          -> Gemini turns every part into a list of numbers (embedding)
          -> keep the parts and their numbers in the user's session

 ASK      question -> Gemini turns it into numbers
          -> score every part: multiply the numbers pair by pair and add them
          -> send the 5 best parts + the question to Gemini -> answer
          (no PDF yet? Gemini answers from general knowledge and says so)

 SUMMARY  the whole PDF text -> Gemini -> a simple summary
```

The uploaded PDF and its text are sent to Google's Gemini service to be processed. The PDF file itself is not saved on the server.

### Key Files | الملفات الرئيسية

| File | Purpose | Lines of Code |
|------|---------|:-------------:|
| app.py | Creates the database tables and shows a different menu before login, after login, and for the admin. | 29 |
| services/database.py | Opens the database and creates the tables from `schema.sql`. | 19 |
| services/user_service.py | Sign up (first user becomes admin), log in, list users. | 51 |
| services/chat_service.py | Create a chat, save a message, list chats, load a chat. | 45 |
| services/contact_service.py | Save and list contact messages. | 24 |
| services/pdf_service.py | Read the PDF text and cut it into parts of 2000 characters. | 24 |
| services/ai_service.py | Gemini: embeddings, the similarity score, the 5 best parts, answers and summaries. | 103 |
| app_pages/home.py | Welcome page with three cards (Upload, Ask, Summarize). | 31 |
| app_pages/login.py | Log in and Sign up forms with simple checks. | 40 |
| app_pages/chat.py | The main screen: PDF upload, summary button, saved chats, and the conversation, with suggested-question pills. | 159 |
| app_pages/contact.py | Contact details and a message form saved to the database. | 30 |
| app_pages/admin.py | Two tabs: the users table and the contact messages. | 30 |
| app_pages/logout.py | Clears the session and goes back home. | 5 |
| data/schema.sql | The four tables. | 37 |

---

## 4. Features & User Flow | الميزات وتدفق المستخدم

<div class="arabic">

</div>

### Feature List | قائمة الميزات

| # | Feature | Description | Status |
|---|---------|-------------|:------:|
| 1 | Sign up | Username, email, password, national ID, job and age. Empty boxes and an already-used username or email are refused with a message. The first person to sign up becomes the admin. | ✅ |
| 2 | Log in and log out | Log in with email and password. Log out forgets everything about the user in this session. | ✅ |
| 3 | Smart menu | Before login the menu shows only Home and Log in; after login it shows Chat, Home, Contact us and Log out; the admin also sees Admin. | ✅ |
| 4 | PDF upload | One PDF at a time. The text is cut into parts of 2000 characters; files with more than 90 parts are refused (to stay inside Gemini's free limit). | ✅ |
| 5 | Questions and answers (RAG) | The 5 parts closest in meaning to the question are found with Gemini embeddings and a simple score, and Gemini answers only from them, with article numbers when possible. | ✅ |
| 6 | Suggested questions | Clickable pills above the question box ("What is this document about?", "What are my rights?", "Are there any deadlines or dates?"...). One click asks the question. | ✅ |
| 7 | Answer language | If the question has Arabic letters the answer is in Arabic, otherwise in English. | ✅ |
| 8 | No PDF? | Gemini answers from general knowledge and says the answer is not from a document. | ✅ |
| 9 | Summary | One button summarizes the whole document in its own language. | ✅ |
| 10 | Saved chats | Every chat is saved; the sidebar lists them so the user can reopen one or start a new chat. | ✅ |
| 11 | Contact us | A message form saved to the database. | ✅ |
| 12 | Admin page | A table of all users and a list of the contact messages. | ✅ |
| 13 | Scanned PDFs | Not supported — the app says the PDF has no readable text. | ❌ |

> Status: ✅ Complete | ⏳ In Progress | ❌ Not Started

> Known limits (kept on purpose to keep the code simple): passwords are stored as plain text, there is no error handling (for example, if Gemini's free quota runs out the page shows an error), and some Arabic PDFs that store their text in visual order come out with words reversed.

### User Flow | تدفق المستخدم

```
   ┌──────────┐     ┌──────────┐
   │   Home   │ ──► │  Log in  │
   └──────────┘     └────┬─────┘
                         │ correct email + password
                    ┌────▼─────┐
                    │   Chat   │ ◄── the start page after login
                    └────┬─────┘
           ┌─────────────┼──────────────┐
      ┌────▼─────┐  ┌────▼─────┐   ┌────▼─────┐
      │ Contact  │  │  Admin   │   │ Log out  │
      │    us    │  │ (admin)  │   │          │
      └──────────┘  └──────────┘   └──────────┘
```

The menu is at the top of the page and only shows the pages the user is allowed to open.

### Screen Reference | دليل الشاشات

| Screen | File | Description | Transitions To |
|--------|------|-------------|----------------|
| Home | `app_pages/home.py` | Title, a "not legal advice" note, three cards (Upload, Ask, Summarize) and a button. | Log in (or Chat if logged in) |
| Log in | `app_pages/login.py` | Two tabs: Log in, and Sign up. | Chat, after logging in |
| Chat | `app_pages/chat.py` | Sidebar: upload a PDF, Summarize button, New chat, saved chats. Main area: the conversation, suggested-question pills, and the question box. | Any page in the menu |
| Contact us | `app_pages/contact.py` | Contact details and a Name / Email / Message form. | Any page in the menu |
| Admin | `app_pages/admin.py` | Tabs: Users (a table) and Contact messages. Admin only. | Any page in the menu |
| Log out | `app_pages/logout.py` | Logs out and returns to Home. | Home |

---

## 5. UI/UX Design | تصميم واجهة المستخدم

<div class="arabic">
هنا تحط لقطات الشاشة + وصف التصميم البصري لمشروعك
</div>

### Screenshots | لقطات الشاشة

<!-- Screenshot: Home page -->
**Home**: The ⚖️ Ma`at title, a blue "not legal advice" note, three bordered cards side by side — Upload, Ask, Summarize — and one "Log in / Sign up" button.

<!-- Screenshot: Log in page -->
**Log in**: Two tabs. "Log in" has Email and Password; "Sign up" has Username, Email, Password, National ID, Job and Age.

<!-- Screenshot: Chat page -->
**Chat**: The sidebar holds the PDF uploader, a green "Ready: file.pdf" note, the "Summarize the document" button, "New chat" and the list of saved chats. The main area shows the conversation as chat bubbles, a row of suggested-question pills, and the question box at the bottom.

<!-- Screenshot: Admin page -->
**Admin**: A table of all users and a tab with the contact messages.

### Design System | نظام التصميم

| Element | Style |
|---------|-------|
| **Colors** | Streamlit's default theme (light or dark, following the user's device). |
| **Font** | Streamlit's default font. |
| **Icons** | Material icons in the menu and buttons (home, chat, mail, upload, summarize). |
| **Buttons** | The main action on each screen is a highlighted "primary" button. |
| **Layout** | A top menu, wide pages, bordered cards on the home page, and a sidebar on the chat page. |

### Responsive Design | التصميم المتجاوب

| Breakpoint | Layout | Tested? |
|------------|--------|:-------:|
| Desktop (1024px+) | Top menu, three cards in a row, chat sidebar open. | ☐ |
| Tablet (768-1024px) | Same layout, narrower. | ☐ |
| Mobile (< 768px) | Cards stack under each other and the chat sidebar folds away behind a button. | ☐ |

---

## 6. Data Sources | مصادر البيانات

<div class="arabic">
هنا تكتب منين جبت الداتا — قاعدة بيانات، API، ملفات، أو داتا مكتوبة في الكود
</div>

### Data Sources | مصادر البيانات

| Source | Type | Description |
|--------|------|-------------|
| Uploaded PDF | User Input | The law, contract or ruling the user uploads. Its text is sent to Google Gemini; the file itself is not saved. |
| Sign-up form | User Input | Username, email, password, national ID, job and age. |
| Chats and contact form | User Input | Questions, answers and messages, saved in the database. |
| Google Gemini | API | Embeddings for searching and the written answers and summaries. |

### Database Schema | مخطط قاعدة البيانات

| Table | Columns | Description |
|-------|---------|-------------|
| `users` | `id`, `username`, `email`, `password`, `ssn`, `job`, `age`, `role`, `created_at` | One row per account. `role` is `admin` for the first user and `user` for everyone else. |
| `chats` | `id`, `user_id`, `title`, `created_at` | One row per saved chat; the title is the start of the first message. |
| `messages` | `id`, `chat_id`, `sender`, `text`, `created_at` | Every question (`user`) and answer (`assistant`). |
| `contact_messages` | `id`, `user_id`, `name`, `email`, `message`, `created_at` | Messages from the Contact us page. |

### External APIs (if any) | واجهات برمجة التطبيقات

| API | Purpose | Rate Limit |
|-----|---------|------------|
| Gemini `gemini-embedding-001` | Turns PDF parts and questions into numbers for searching. | Free plan: about 100 parts per minute, and a daily limit — that is why big PDFs are refused. |
| Gemini `gemini-2.5-flash` | Writes the answers and summaries. | Depends on the Google AI Studio plan. |

The API key is kept in `.streamlit/secrets.toml` (never in the code).

---

## 7. Educational Content | المحتوى التعليمي

<div class="arabic">
هنا تكتب المحتوى التعليمي — ماذا يتعلم الطالب من هذا المشروع؟ كيف يتعلق بالمنهج؟
</div>

### Learning Objectives | أهداف التعلم

By the end of this project, the student will be able to:

1. Explain and build a **simple RAG system**: cut a document into parts, find the parts that match a question, and ask an AI to answer only from them.
2. Explain **embeddings**: how an AI turns text into a list of numbers, and how multiplying two lists and adding the results measures how close two meanings are.
3. **Write clear prompts**: tell the AI which text to use, which language to answer in, and to say "I don't know" instead of inventing.
4. **Use a database** with SQLite: create tables, add rows, and find rows with `SELECT ... WHERE`.
5. **Build a multi-page website** with Streamlit: pages, a menu, forms, tabs, chat bubbles, and `st.session_state` to remember the logged-in user.
6. **Keep a secret safe**: the API key lives in a secrets file, not in the code.

### Cultural / Historical Context | السياق الثقافي / التاريخي

| Topic | Description |
|-------|-------------|
| The name "Ma`at" | Ma`at (also written Ma'at) is the ancient Egyptian idea of truth, justice, and the order that keeps the world and society together, traditionally shown as a woman holding the scales of justice — the ⚖️ emoji in the app's title. The project takes the name because it is about the same thing: making the law fair to read, so that a person can weigh what a document says instead of taking it on trust. |
| Access to law in Egypt | Egyptian law is published in long, formal Arabic, and a contract or a ruling is often hundreds of pages long, so understanding it normally means paying for a lawyer or giving up. Ma`at lets a law student, a citizen, or a small firm upload the actual document and ask a plain question in Arabic or English — bringing the law closer to the people it applies to, in both languages. |

### Curriculum Alignment | التوافق مع المنهج

| Skill Area | What the Student Practices |
|------------|---------------------------|
| Problem Solving | Turning "laws are hard to read" into steps: upload, cut, search, answer. |
| Computational Thinking | Loops, lists, simple functions, and a scoring algorithm that picks the best 5 parts. |
| Creativity | Designing a clear menu and screens that show only what each user needs. |
| Collaboration | Using an online AI service (Gemini) and following its rules and limits. |
| Technical Writing | The README and this bilingual document. |

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
| Libraries | pypdf, google-genai |

---

### My Screens | شاشات مشروعي

Draw or describe all the screens in your project:

| Screen Name | What the user sees/does | How to get here |
|-------------|------------------------|-----------------|
| Home | Title, three cards and a Log in button. | Open the app |
| Log in | Log in and Sign up tabs. | The Home button, or the top menu |
| Chat | Upload a PDF, ask questions, summarize, saved chats. | Automatically after logging in |
| Contact us | Contact details and a message form. | Top menu, after logging in |
| Admin | Users table and contact messages. | Top menu, admin only |

---

### My Features | ميزات مشروعي

| Feature | What it does | Status |
|---------|-------------|:------:|
| Sign up / Log in | Creates an account and logs in; the first user is the admin. | ✅ |
| Upload a PDF | Reads the text and cuts it into parts. | ✅ |
| Ask questions | Finds the 5 best parts with embeddings and Gemini answers from them. | ✅ |
| Summary | Summarizes the whole document. | ✅ |
| Saved chats | Reopen old chats from the sidebar. | ✅ |
| Contact us | Sends a message to the admin. | ✅ |
| Admin page | Shows users and messages. | ✅ |

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
