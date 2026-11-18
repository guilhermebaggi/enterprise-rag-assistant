
from app.services.document_loader import extract_text_from_pdf
from app.services.chunking import create_document_chunks


pages = extract_text_from_pdf(
    "documents/documento_teste.pdf"
)

chunks = create_document_chunks(
    pages,
    chunk_size=1000,
    overlap=200
)

print("Total de páginas:", len(pages))
print("Total de chunks:", len(chunks))

for item in chunks[:5]:

    print("\n----------------------------")
    print("Página:", item["page"])
    print("Chunk:", item["chunk"])
    print("Caracteres:", len(item["text"]))
    print(item["text"][:200])
