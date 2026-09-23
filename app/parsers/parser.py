from pathlib import Path

from app.ingestion.file_detector import detect_file_type
from app.models.document import Document
from app.parsers.html_parser import parse_html
from app.parsers.pdf_parser import parse_pdf


def parse_document(file_path: Path) -> Document:
    """
    Parse a supported document and return a normalized Document object.
    """

    file_type = detect_file_type(file_path)

    if file_type == "html":
        text = parse_html(file_path)

    elif file_type == "pdf":
        text = parse_pdf(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {file_path}"
        )

    return Document(
        document_id=file_path.stem,
        filename=file_path.name,
        source_folder=file_path.parent.name,
        file_type=file_type,
        text=text
    )