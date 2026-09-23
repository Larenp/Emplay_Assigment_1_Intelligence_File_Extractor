from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".html",
    ".htm",
    ".pdf"
}


def scan_directory(directory: str) -> list[Path]:
    """
    Recursively find supported documents inside a directory.
    """

    root = Path(directory)

    if not root.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {directory}"
        )

    files = []

    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)

    return sorted(files)


def scan_input_folders(input_directory: str) -> list[Path]:
    """
    Scan all folders inside the input directory.
    """

    root = Path(input_directory)

    if not root.exists():
        raise FileNotFoundError(
            f"Input directory does not exist: {input_directory}"
        )

    documents = []

    for folder in root.iterdir():
        if not folder.is_dir():
            continue

        documents.extend(
            scan_directory(str(folder))
        )

    return sorted(documents)