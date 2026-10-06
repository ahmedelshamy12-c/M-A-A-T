"""Application services.

Loading `.env` here (instead of only in `app.py`) means the API key and admin
settings are available even when the first page a visitor opens is not the
landing page — Streamlit runs each page file on its own.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
