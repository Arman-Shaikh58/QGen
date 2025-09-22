from pypdf import PdfReader
from llm_config import create_questions
from typing import Dict, Any


def read_pdf(file_path: str) -> Dict[str, Any]:
    """
    Reads a PDF file and returns the questions dictionary produced from its text.

    :param file_path: Path to the PDF file.
    :return: Questions dictionary returned by `create_questions` or an error dict.
    """
    try:
        reader = PdfReader(file_path)
    except Exception as e:
        return {"error": f"Failed to open PDF: {e}"}

    pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages.append(page_text)

    full_text = "\n".join(pages).strip()

    if not full_text:
        return {"2_marks": [], "4_marks": [], "6_marks": []}

    questions = create_questions(full_text)
    return questions

