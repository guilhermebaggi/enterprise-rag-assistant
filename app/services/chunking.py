
def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Divide um texto em chunks com sobreposição.

    Args:
        text: Texto original.
        chunk_size: Quantidade máxima de caracteres por chunk.
        overlap: Quantidade de caracteres repetidos entre chunks.

    Returns:
        Lista de fragmentos de texto.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size deve ser maior que zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap deve ser >= 0 e menor que chunk_size.")

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_document_chunks(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[dict]:
    """
    Cria chunks mantendo os metadados da página original.
    """

    all_chunks = []

    for page in pages:

        page_chunks = split_text(
            page["text"],
            chunk_size,
            overlap
        )

        for chunk_number, chunk_text in enumerate(page_chunks, start=1):

            all_chunks.append({
                "page": page["page"],
                "chunk": chunk_number,
                "text": chunk_text
            })

    return all_chunks
