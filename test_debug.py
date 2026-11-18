from app.services.document_loader import extract_text_from_pdf
from app.services.retriever import Retriever

pdf_path = "documents/documento_teste.pdf"

# 1. Verificar o texto extraído do PDF
print("\n========== TEXTO EXTRAÍDO DO PDF ==========")

pages = extract_text_from_pdf(pdf_path)

for page in pages:
    print(f"\n{'=' * 20} PÁGINA {page['page']} {'=' * 20}")
    print(page["text"])


# 2. Verificar os chunks recuperados pelo RAG
query = "Quais são as taxas cobradas no condomínio?"

retriever = Retriever(top_k=5)
results = retriever.retrieve(query)

print("\n========== CHUNKS RECUPERADOS ==========")

for index, result in enumerate(results, start=1):
    print(f"\nResultado {index}")
    print(f"Documento: {result['source']}")
    print(f"Página: {result['page']}")
    print(f"Chunk: {result['chunk']}")
    print(f"Similaridade: {result['score']:.4f}")
    print("\nConteúdo completo:")
    print(result["text"])
    print("-" * 80)
