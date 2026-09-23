from pathlib import Path


def detect_file_type(file_path: Path) -> str:
    """
    Detect the supported document type from its extension.
    """

    extension = file_path.suffix.lower()

    if extension in {".html", ".htm"}:
        return "html"

    if extension == ".pdf":
        return "pdf"

    return "unknown"