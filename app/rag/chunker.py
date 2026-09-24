def create_chunks(
    sections: list[dict],
    chunk_size: int = 250,
    overlap: int = 50
) -> list[str]:
    """
    Create chunks from document sections with overlap.
    """

    chunks = []

    for section in sections:
        text = " ".join(section["content"])
        words = text.split()

        if not words:
            continue

        # Small section: keep it as one chunk
        if len(words) <= chunk_size:
            chunks.append(
                f"{section['title']}\n{text}"
            )
            continue

        # Large section: split with overlap
        start = 0

        while start < len(words):
            end = start + chunk_size

            chunk_text = " ".join(words[start:end])

            chunks.append(
                f"{section['title']}\n{chunk_text}"
            )

            if end >= len(words):
                break

            start = end - overlap

    return chunks