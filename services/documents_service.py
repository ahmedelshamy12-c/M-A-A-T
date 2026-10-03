"""Turn uploaded PDFs into a searchable index.

PDF -> plain text -> overlapping chunks -> FAISS vector store.

Embeddings come from Gemini rather than a local sentence-transformers model:
the old `all-MiniLM-L6-v2` model is English-only (and pulls in torch), which
gave useless retrieval on Arabic legal text.
"""

import os

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def get_embeddings():
    """Gemini embedding model, configured from the environment.

    `GOOGLE_API_KEY` is read from the environment by langchain-google-genai.
    """
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    )


def get_pdf_text(pdf_docs):
    """Concatenate the text of every page of every given PDF.

    Pages are joined with a newline, otherwise the last word of one page fuses
    with the first word of the next one.
    """
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF {getattr(pdf, 'name', pdf)}: {e}")
    return text


def get_text_chunks(text):
    """Split text into overlapping chunks for retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    """FAISS index over the chunks, or None if there is nothing to index."""
    if not text_chunks:
        return None

    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=get_embeddings())
    return vectorstore


def build_vectorstore(pdf_files):
    """Uploaded PDF files -> FAISS index, or None if no text could be read.

    Convenience wrapper for the three steps above, so pages only deal with
    files and a vector store (or None for scanned, image-only PDFs).
    """
    return get_vectorstore(get_text_chunks(get_pdf_text(pdf_files)))