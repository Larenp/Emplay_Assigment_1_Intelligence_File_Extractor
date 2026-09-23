from pathlib import Path

import pymupdf


def parse_pdf(file_path: Path) -> str:
    """
    Extract text from all pages of a PDF document.
    """

    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text("text")

        if text.strip():
            pages.append(
                f"[PAGE {page_number + 1}]\n{text.strip()}"
            )

    document.close()

    return "\n\n".join(pages)
    
