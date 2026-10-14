
## #10 [feature] Suggested questions as pills
- `st.pills` above the chat box with a fixed English list (`SUGGESTED_QUESTIONS` in `app_pages/chat.py`); shown always; one click asks the question; the pill resets so it can be clicked again.
- Status: done — awaiting commit

## #11 [docs] Competition poster (100×200 cm roll-up)
- Portrait 1000×2000 mm vector PDF built from HTML (+5 mm bleed, 30 mm safe margin, bottom 100 mm empty for the stand), English only.
- Hero art is a vector illustration (no Higgsfield).
- Brand: feather-of-Ma'at logo, Nile & gold palette (cream `#F3EAD7`, lapis `#14213D`, Nile `#1F4E79`, gold `#C9962B`, turquoise `#2F7D6B`), tagline "Justice, explained."
- Sections: hero (vector feather art + wordmark) → problem/solution → how it works (RAG flow + architecture diagrams, re-skinned) → app screenshot (Arabic Q&A on a sample contract) → tech, credits (Ahmed Medhat, Techno Future, Afro-Asian Technology Competition 2026, ahedmedhat@gmail.com), QR placeholder, not-legal-advice line.
- Follow-up: deploy to Streamlit Cloud and swap the real QR code in before printing.
- Demo document is a sample Arabic employment contract (`docs/poster/demo/`), not a law excerpt: the text of the new Labour Law 14/2025 couldn't be verified.
- Status: draft done (`docs/poster/`) — awaiting review, real QR code and print-shop spec

## #12 [docs] Ma‘at logo
- Kneeling Ma'at with spread wings and the feather of truth, in her original tomb-painting colors and feather detail (flat vector), on lapis plus a cream version, serif wordmark "Ma‘at", simplified emblem for the favicon.
- Prompts for GPT Image in `docs/brand/logo-prompts.md` (symbol, 2 lockups, app icon).
- Follow-up: generate, pick a version, then use it in the poster hero and as `page_icon` in `app.py`.
- Generated images in `docs/assets/`. Master mark (background cut out) is in the poster hero (`docs/poster/assets/maat-mark.png`); app icon resized to `images/icon.png` and used as `page_icon`.
- Status: done — awaiting commit
