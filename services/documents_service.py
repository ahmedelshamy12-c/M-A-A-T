"""Turn uploaded PDFs into a searchable index.

PDF -> plain text -> overlapping chunks -> FAISS vector store.

Embeddings come from Gemini rather than a local sentence-transformers model:
the old `all-MiniLM-L6-v2` model is English-only (and pulls in torch), which
gave useless retrieval on Arabic legal text.
"""

import os
import re
import time
import unicodedata
from itertools import groupby

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DEFAULT_EMBEDDING_MODEL = "gemini-embedding-2"


def get_embeddings():
    """Gemini embedding model, configured from the environment.

    `GOOGLE_API_KEY` is read from the environment by langchain-google-genai.
    """
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    )


# Arabic presentation forms (contextual glyph shapes). PDFs that store Arabic
# this way also store it in visual order, so pypdf returns each line with its
# words reversed: "ﻣﺼﺮ دﺳﺘﻮر" instead of "دستور مصر".
_PRESENTATION_FORMS = re.compile("[\uFB50-\uFDFF\uFE70-\uFEFF]")
_ARABIC = re.compile("[\u0600-\u06FF]")

# Table-of-contents lines ("Article 5 ........ 12") match almost any question
# and crowd the real articles out of the search results.
_DOT_LEADER = re.compile(r"\.{5,}|…{2,}")


def fix_visual_arabic(line):
    """Turn a visually ordered Arabic line back into normal (logical) text.

    Only lines containing presentation-form glyphs are touched: the glyphs are
    mapped to ordinary letters (NFKC) and the word order is reversed, while
    runs of non-Arabic words (numbers, Latin text) keep their own order.
    """
    if not _PRESENTATION_FORMS.search(line):
        return line

    words = unicodedata.normalize("NFKC", line).split()
    runs = [
        (is_arabic, list(group))
        for is_arabic, group in groupby(words, key=lambda w: bool(_ARABIC.search(w)))
    ]
    ordered = []
    for is_arabic, group in reversed(runs):
        ordered.extend(reversed(group) if is_arabic else group)
    return " ".join(ordered)


def get_pdf_text(pdf_docs):
    """Concatenate the text of every page of every given PDF.

    Pages are joined with a newline, otherwise the last word of one page fuses
    with the first word of the next one. Visually ordered Arabic lines are
    repaired with `fix_visual_arabic`, and table-of-contents lines (dot
    leaders) are dropped.
    """
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    lines = [
                        fix_visual_arabic(line)
                        for line in page_text.split("\n")
                        if not _DOT_LEADER.search(line)
                    ]
                    text += "\n".join(lines) + "\n"
        except Exception as e:
            print(f"Error reading PDF {getattr(pdf, 'name', pdf)}: {e}")
    return text


# Fewer, larger chunks keep a long law within the embedding quota; each chunk
# is still far below the embedding model's input limit.
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 250

# The Gemini free tier allows 100 embedded chunks per minute, so chunks are
# embedded in batches and a rate-limit error waits for the quota to refill.
EMBED_BATCH_SIZE = 50
EMBED_MAX_ATTEMPTS = 5
DEFAULT_RETRY_SECONDS = 60
_RETRY_IN = re.compile(r"retry in ([\d.]+)s", re.IGNORECASE)


def get_text_chunks(text):
    """Split text into overlapping chunks for retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


RATE_LIMIT_MESSAGE = (
    "The Gemini free-tier quota is used up for the moment. "
    "Please wait a minute and try again."
)


def is_rate_limit(error):
    """True for Gemini quota / rate-limit (HTTP 429) errors."""
    message = str(error)
    return "RESOURCE_EXHAUSTED" in message or "429" in message


def _retry_seconds(error):
    match = _RETRY_IN.search(str(error))
    return float(match.group(1)) + 1 if match else DEFAULT_RETRY_SECONDS


def retry_on_rate_limit(fn, *args, attempts=EMBED_MAX_ATTEMPTS, sleep=time.sleep, **kwargs):
    """Call `fn`, waiting out Gemini rate limits between attempts.

    Any other error is raised immediately; a rate limit is raised once
    `attempts` calls have failed.
    """
    for attempt in range(1, attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            if not is_rate_limit(error) or attempt == attempts:
                raise
            sleep(_retry_seconds(error))


def _embed_batch(embeddings, texts, sleep=time.sleep):
    """Embed one batch, waiting and retrying when the quota is exhausted."""
    return retry_on_rate_limit(embeddings.embed_documents, texts, sleep=sleep)


def get_vectorstore(text_chunks, progress=None):
    """FAISS index over the chunks, or None if there is nothing to index.

    `progress`, if given, is called with the fraction of chunks embedded so
    far (0..1) after each batch — indexing a long law can take a few minutes
    on the free tier.
    """
    if not text_chunks:
        return None

    embeddings = get_embeddings()
    vectorstore = None
    total = len(text_chunks)
    for start in range(0, total, EMBED_BATCH_SIZE):
        batch = text_chunks[start : start + EMBED_BATCH_SIZE]
        pairs = list(zip(batch, _embed_batch(embeddings, batch)))
        if vectorstore is None:
            vectorstore = FAISS.from_embeddings(pairs, embeddings)
        else:
            vectorstore.add_embeddings(pairs)
        if progress:
            progress(min(start + EMBED_BATCH_SIZE, total) / total)
    return vectorstore


def index_text(text, progress=None):
    """Document text -> FAISS index, or None if there is no text to index.

    The chat page keeps the extracted text too (for summaries), so it calls
    `get_pdf_text` itself and passes the result here.
    """
    return get_vectorstore(get_text_chunks(text), progress=progress)
