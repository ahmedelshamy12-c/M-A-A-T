import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables (like API keys)
load_dotenv()

st.set_page_config(
    page_title=" Ma`at ", page_icon="⚖️", layout="wide"
)

# Custom Styling
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            color: #2c3e50;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 2rem;
            font-size: 1.2rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Main Interface
st.markdown(
    "<h1 class='main-title'>⚖️ Ma`at</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p class='subtitle'>Smart System for Assisting with Understanding Egyptian Legal Documents</p>",
    unsafe_allow_html=True,
)

# Introduction
st.info(
    "💡 This assistant provides general information for assistance, but is not a replacement for legal advice from a qualified attorney."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Document Summarization")
    st.write("Upload PDF files (laws, contracts, rulings) and get instant summaries.")

with col2:
    st.markdown("### 💬 Ask the Assistant")
    st.write("Ask any question about your documents and the system will provide answers.")

st.divider()

# Call to Action
st.write("### To get started, please log in or create a new account")

if st.button("Log in / Create Account", type="primary"):
    st.switch_page("pages/auth.py")
