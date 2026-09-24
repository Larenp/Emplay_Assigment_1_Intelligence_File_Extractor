def create_chunks(
    sections: list[dict],
    chunk_size: int = 250,
    overlap: int = 50,
) -> list[str]:

    chunks = []

    # Combine all section content into one document.
    document_parts = []

    for section in sections:
        title = section.get("title", "")
        content = section.get("content", [])

        if title:
            document_parts.append(title)

        document_parts.extend(content)

    words = " ".join(document_parts).split()

    if not words:
        return []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_text = " ".join(words[start:end])

        chunks.append(chunk_text)

        if end >= len(words):
            break

        start = end - overlap

    return chunks