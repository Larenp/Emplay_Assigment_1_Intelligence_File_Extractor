from pathlib import Path

from bs4 import BeautifulSoup


def parse_html(file_path: Path) -> str:
    """
    Extract readable text from an HTML document.
    """

    html = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(html, "lxml")

    # Remove elements that do not contain useful document content
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text(separator="\n")

    # Clean empty lines and unnecessary whitespace
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)
    