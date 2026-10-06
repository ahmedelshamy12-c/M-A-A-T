# Reading a PDF and cutting its text into parts.

from pypdf import PdfReader

PART_SIZE = 2000  # how many characters go in one part of the PDF
MAX_PARTS = 90  # the free Gemini plan can embed about 100 parts per minute


def read_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text = text + page_text + "\n"
    return text


def split_text(text):
    # Cut the text into parts of PART_SIZE characters.
    parts = []
    for start in range(0, len(text), PART_SIZE):
        parts.append(text[start : start + PART_SIZE])
    return parts
