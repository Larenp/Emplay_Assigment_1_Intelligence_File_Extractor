from pathlib import Path


def detect_file_type(file_path: Path) -> str:
    """
    Detect the document type based on its file extension.
    """

    extension = file_path.suffix.lower()

    if extension in {".html", ".htm"}:
        return "html"

    if extension == ".pdf":
        return "pdf"

    return "unknown"