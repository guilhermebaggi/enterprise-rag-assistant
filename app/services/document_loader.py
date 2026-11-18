from pathlib import Path
import pymupdf

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extrai o texto de cada página de um arquivo PDF.

    Args:
        pdf_path: Caminho do arquivo PDF.

    Returns:
        Lista de dicionários contendo o número da página e seu texto.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("O arquivo informado não é um PDF.")

    pages = []

    with pymupdf.open(path) as document:

        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text
                })

    return pages
