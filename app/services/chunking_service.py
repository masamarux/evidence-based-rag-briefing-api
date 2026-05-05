def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 120,
) -> list[str]:
    normalized_text = " ".join(text.split())

    if not normalized_text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(normalized_text):
        end = start + chunk_size
        chunk = normalized_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(normalized_text):
            break

        start = end - overlap

    return chunks