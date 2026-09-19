
# Software Project Documentation | توثيق مشروع البرمجيات

<div class="arabic">
قالب توثيق مشاريع البرمجيات — للمسابقة الأفريقية الآسيوية للتكنولوجيا
</div>

---

## 1. Project Overview | نظرة عامة على المشروع

| Field | Value |
|-------|-------|
| **Project Title** | [] |
| **Project Type** | [Web App /  AI Tool ] |
| **Description** | [This is a Ai tool for helping people understanding Egyption law.An AI_powerd app legal website bilt with rag for egyption law ] |
| **Target Users** | [law students ., Egyptian citizinens,researchers,small lawyers] |
| **Resolution / Platform** | [ mobile-responsive, ] |
| **Date** | [9/8/2026] |

### Tech Stack | Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | [Python] | [make the project] |
| **Framework** | [ Streamlit] | [make it simple to biuld the website] |
| **Database** | [SQLite] | [save data] |
| **Libraries** | [] | [what they do] |
| [google-generativeai] | [,langchain] | [faiss-cpu] |

### Dependencies | المكتبات المستخدمة

| Package | Version | Purpose |
|---------|---------|---------|
| [fill in] | [fill in] | [fill in] |
| [fill in] | [fill in] | [fill in] |

<!-- Screenshot: Main screen of your project -->

---

## 2. Problem Statement | بيان المشكلة

<div class="arabic">ن كتير من الناس في مصر بتواجه صعوبة كبيرة في فهم النصوص القانونية بسبب تعقيد اللغة وطول المواد.
</div>

### What problem does this project solve? | ما المشكلة التي يحلها هذا المشروع؟

[ن كتير من الناس في مصر بتواجه صعوبة كبيرة في فهم النصوص القانونية بسبب تعقيد اللغة وطول المواد.,]

### Why does it matter? | لماذا هذا مهم؟

becaus it sempelyfy egyptoin law 
### How is it currently solved? | كيف تُحل المشكلة حالياً؟

[I make this ai tool]


---

## 3. Technical Architecture | البنية التقنية

<div class="arabic">
هنا تشرح كيف مشروعك مبني من الداخل — هيكل الملفات والتقنيات المستخدمة
</div>

### Project Structure | هيكل المشروع

```
project-name/
├── app.py              # Entry point
├── pages/           #  python
│   ├── auth.py,chat.py ,contact_us.py
│   └── home.py , view_users.py
├── services/              # python
│   ├── documents.py
│   └── chat.py , auth.py
├── data/            # Database files
│   └── data_base.db , egy_law_tables.sql
├── requirements.txt     # Python dependencies
└── README.md            # (optional)
```

[Replace the above with your actual project structure]

### Architecture Diagram | مخطط البنية

```
[User] → [Frontend] → [Backend] → [Database]
```

[Draw or describe your architecture — how do the parts connect?]

### Key Files | الملفات الرئيسية

| File | Purpose | Lines of Code |
|------|---------|:-------------:|
| [fill in] | [what it does] | [approximate] |
| [fill in] | [what it does] | [approximate] |
| [fill in] | [what it does] | [approximate] |

---

## 4. Features & User Flow | الميزات وتدفق المستخدم

<div class="arabic">

</div>

### Feature List | قائمة الميزات

| # | Feature | Description | Status |
|---|---------|-------------|:------:|
| 1 | [fill in] | [what it does] | ✅ / ⏳ / ❌ |
| 2 | [fill in] | [what it does] | ✅ / ⏳ / ❌ |
| 3 | [fill in] | [what it does] | ✅ / ⏳ / ❌ |
| 4 | [fill in] | [what it does] | ✅ / ⏳ / ❌ |
| 5 | [fill in] | [what it does] | ✅ / ⏳ / ❌ |

> Status: ✅ Complete | ⏳ In Progress | ❌ Not Started

### User Flow | تدفق المستخدم

```
                    ┌──────────────┐
                    │   LANDING    │
                    │    PAGE      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   LOGIN /    │
                    │   REGISTER   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   DASHBOARD  │
                    │  (main hub)  │
                    └──┬───┬───┬───┘
                       │   │   │
              ┌────────┘   │   └────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Screen 1 │ │ Screen 2 │ │ Screen 3 │
        │ (name)   │ │ (name)   │ │ (name)   │
        └──────────┘ └──────────┘ └──────────┘
```

[Replace with your actual user flow]

### Screen Reference | دليل الشاشات

| Screen | File / Route | Description | Transitions To |
|--------|-------------|-------------|----------------|
| [fill in] | [fill in] | [what user sees/does] | [where they can go] |
| [fill in] | [fill in] | [what user sees/does] | [where they can go] |
| [fill in] | [fill in] | [what user sees/does] | [where they can go] |

---

## 5. UI/UX Design | تصميم واجهة المستخدم

<div class="arabic">
هنا تحط لقطات الشاشة + وصف التصميم البصري لمشروعك
</div>

### Screenshots | لقطات الشاشة

<!-- Screenshot: Landing page -->
**Landing Page**: [describe what the user sees]

<!-- Screenshot: Main dashboard -->
**Dashboard**: [describe what the user sees]

<!-- Screenshot: Key feature screen -->
**Key Feature**: [describe what the user sees]

<!-- Add more screenshots as needed -->

### Design System | نظام التصميم

| Element | Style |
|---------|-------|
| **Primary Color** | [e.g., rgb(2, 2, 2) (black)] |
| **Secondary Color** | [e.g., rgb(77, 84, 78) (gray)] |
| **Font** | [e.g., Inter, Arial, Cairo] |
| **Button Style** | [e.g., rounded, flat, gradient] |
| **Layout** | [e.g., sidebar navigation, top navbar, cards] |

### Responsive Design | التصميم المتجاوب

| Breakpoint | Layout | Tested? |
|------------|--------|:-------:|
| Desktop (1024px+) | [describe layout] | ☐ |
| Tablet (768-1024px) | [describe layout] | ☐ |
| Mobile (< 768px) | [describe layout] | ☐ |

---

## 6. Data Sources | مصادر البيانات

<div class="arabic">
هنا تكتب منين جبت الداتا — قاعدة بيانات، API، ملفات، أو داتا مكتوبة في الكود
</div>

### Data Sources | مصادر البيانات

| Source | Type | Description |
|--------|------|-------------|
| [fill in] | [Database / API / JSON / Static / User Input] | [what data it provides] |
| [fill in] | [fill in] | [fill in] |
| [fill in] | [fill in] | [fill in] |

### Database Schema | مخطط قاعدة البيانات

| Table | Columns | Description |
|-------|---------|-------------|
| [fill in] | [fill in] | [what it stores] |
| [fill in] | [fill in] | [what it stores] |

### External APIs (if any) | واجهات برمجة التطبيقات

| API | Purpose | Rate Limit |
|-----|---------|------------|
| [fill in] | [what it's used for] | [requests per day/hour] |

---

## 7. Educational Content | المحتوى التعليمي

<div class="arabic">
هنا تكتب المحتوى التعليمي — ماذا يتعلم الطالب من هذا المشروع؟ كيف يتعلق بالمنهج؟
</div>

### Learning Objectives | أهداف التعلم

By the end of this project, the student will be able to:

1. [fill in — e.g., Build a full-stack web application with Python]
2. [fill in — e.g., Design and query a SQLite database]
3. [fill in — e.g., Create responsive UI with HTML/CSS]
4. [fill in — e.g., Implement user authentication]
5. [fill in]

### Cultural / Historical Context | السياق الثقافي / التاريخي

| Topic | Description |
|-------|-------------|
| [Theme of your project] | [How does it connect to culture, science, or society?] |
| [fill in] | [fill in] |

### Curriculum Alignment | التوافق مع المنهج

| Skill Area | What the Student Practices |
|------------|---------------------------|
| Problem Solving | [e.g., Breaking a real problem into code solutions] |
| Computational Thinking | [e.g., Data modeling, algorithms, abstraction] |
| Creativity | [e.g., UI design, user experience, visual storytelling] |
| Collaboration | [e.g., Pair programming, code reviews] |
| Technical Writing | [e.g., Documenting architecture and features] |

---

## 8. Marketing Plan | خطة تسويقية

> **Short version** — for full marketing plans, use the main Afro-Asian template.

<div class="arabic">Short marketing plan: target law students, Egyptian citizens, researchers, and small legal practitioners; promote the website through social media, WhatsApp, university groups, and legal communities; share demo videos, simple legal explainers, FAQs, and screenshots to show how the app makes Egyptian law easier to understand, while building trust and increasing visits and engagement.


</div>

### Target Audience | الجمهور المستهدف

- **Primary**: [who will use this — e.g., law students ]
- **Secondary**: [who else — e.g., ]
- **Tertiary**: [anyone else — e.g., health organizations, coding communities]

### Platforms | المنصات

- [e.g., Web browser (Chrome, Firefox, Edge)]
- [e.g., Mobile phone]
- [e.g., School computers]

### Promotion Ideas | أفكار ترويجية

1. [e.g., Share demo video on YouTube/TikTok]
2. [e.g., Present at school science fair]
3. [e.g., Post screenshots on class group]
4. [e.g., Submit to Afro-Asian Tech Forum competition]

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
| Language | |
| Framework | |
| Database | |
| Libraries | |

---

### My Screens | شاشات مشروعي

Draw or describe all the screens in your project:

| Screen Name | What the user sees/does | How to get here |
|-------------|------------------------|-----------------|
| | | |
| | | |
| | | |

---

### My Features | ميزات مشروعي

| Feature | What it does | Status |
|---------|-------------|:------:|
| | | ✅ / ⏳ / ❌ |
| | | ✅ / ⏳ / ❌ |
| | | ✅ / ⏳ / ❌ |

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
