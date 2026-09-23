import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):

        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def detect_sections(text: str) -> list[dict]:
    """
    Split text using numbered headings.
    """

    lines = text.splitlines()

    sections = []
    current_section = None

    for line in lines:

        # Examples:
        # 1 Header Information
        # 1.1 General Information
        # 2.1 Line Information
        if re.match(r"^\d+(?:\.\d+)*\s+.+", line):

            if current_section:
                sections.append(current_section)

            current_section = {
                "title": line,
                "content": []
            }

        elif current_section:
            current_section["content"].append(line)

    if current_section:
        sections.append(current_section)

    return sections


def process_text(text: str) -> dict:
    """
    Clean text and detect sections.
    """

    cleaned_text = clean_text(text)

    sections = detect_sections(cleaned_text)

    return {
        "cleaned_text": cleaned_text,
        "sections": sections
    }