import os
import streamlit as st
import google.generativeai as genai


def get_ai_response(
    user_question: str, *, vectorstore=None, model_name: str = "gemini-2.5-flash"
) -> str:

    try:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            return "Error: GOOGLE_API_KEY was not found in the environment variables"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)

        vs = vectorstore
        if vs is None:
            vs = st.session_state.get("vectorstore")

        context = ""
        found_info = False

        if vs:
            results = vs.similarity_search(user_question, k=3)
            for doc in results:
                if getattr(doc, "page_content", "").strip():
                    found_info = True
                    context += doc.page_content + "\n"

        if found_info:
            instructions = f"""
You are a specialized Egyptian legal assistant.

Use only the following information from the PDF:
{context}

Rules:
- Answer in English
- Mention article numbers when possible
- This is not an official legal consultation

User question:
{user_question}
"""
        else:
            instructions = f"""
No answer was found in the PDF.

- Answer based on general knowledge
- Inform the user that the answer is not from the file

User question:
{user_question}
"""
        response = model.generate_content(instructions)
        return getattr(response, "text", "") or ""

    except Exception as e:
        return f"Error: {str(e)}"
