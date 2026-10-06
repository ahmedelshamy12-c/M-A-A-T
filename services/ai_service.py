# Talking to Google Gemini: finding the best parts, answering, summarizing.

import streamlit as st
from google import genai

CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"
BEST_PARTS_COUNT = 5  # how many parts we send to Gemini with each question


def get_gemini():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])


def embed(texts):
    # Gemini turns every text into a list of numbers (an "embedding").
    # Texts with similar meaning get similar numbers.
    gemini = get_gemini()
    vectors = []
    for text in texts:
        result = gemini.models.embed_content(model=EMBEDDING_MODEL, contents=text)
        vectors.append(result.embeddings[0].values)
    return vectors


def similarity(vector_a, vector_b):
    # Multiply the numbers pair by pair and add them up.
    # The bigger the result, the closer the meaning.
    total = 0
    for a, b in zip(vector_a, vector_b):
        total = total + a * b
    return total


def find_best_parts(question, parts, vectors):
    question_vector = embed([question])[0]
    scores = []
    for i in range(len(parts)):
        score = similarity(question_vector, vectors[i])
        scores.append((score, parts[i]))
    scores.sort(reverse=True)  # highest score first
    best_parts = []
    for score, part in scores[:BEST_PARTS_COUNT]:
        best_parts.append(part)
    return best_parts


def has_arabic(text):
    for letter in text:
        if "؀" <= letter <= "ۿ":
            return True
    return False


def answer_language(question):
    if has_arabic(question):
        return "Write the whole answer in Arabic."
    return "Write the whole answer in English, even if the document is in Arabic."


def ask_gemini(prompt):
    gemini = get_gemini()
    response = gemini.models.generate_content(model=CHAT_MODEL, contents=prompt)
    return response.text


def answer_question(question, best_parts):
    if best_parts:
        prompt = (
            "You help people understand Egyptian law.\n"
            "Answer the question using ONLY these parts of the user's document.\n"
            "Mention the article numbers when you can.\n"
            "If the parts do not contain the answer, say so.\n"
            + answer_language(question)
            + "\nEnd with one line saying this is not legal advice.\n\n"
            + "Parts of the document:\n"
            + "\n---\n".join(best_parts)
            + "\n\nQuestion: "
            + question
        )
    else:
        prompt = (
            "You help people understand Egyptian law.\n"
            "The user has not uploaded a document, so answer from general "
            "knowledge and say that the answer is not from a document.\n"
            + answer_language(question)
            + "\nEnd with one line saying this is not legal advice.\n\n"
            + "Question: "
            + question
        )
    return ask_gemini(prompt)


def summarize(text):
    prompt = (
        "Summarize this legal document for someone who is not a lawyer.\n"
        "Write the summary in the same language as the document.\n"
        "Start with one sentence about what the document is, then list the "
        "key points (rights, duties, deadlines, penalties) with article numbers.\n"
        "End with one line saying this is not legal advice.\n\n"
        "Document:\n" + text
    )
    return ask_gemini(prompt)
