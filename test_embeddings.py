
from app.services.document_loader import extract_text_from_pdf
from app.services.chunking import create_document_chunks
from app.services.embeddings import EmbeddingService

# 1. Extrair o texto do PDF
pages = extract_text_from_pdf(
    "documents/documento_teste.pdf"
)

# 2. Dividir o documento em chunks
chunks = create_document_chunks(
    pages,
    chunk_size=1000,
    overlap=200
)

# 3. Carregar o modelo
embedding_service = EmbeddingService()

# 4. Extrair somente os textos dos chunks
texts = [chunk["text"] for chunk in chunks]

# 5. Gerar embeddings
vectors = embedding_service.encode_documents(texts)

# 6. Verificar os resultados
print("\n========== RESULTADOS ==========")

print("Total de chunks:", len(chunks))
print("Total de embeddings:", len(vectors))

if vectors:
    print("Dimensões do embedding:", len(vectors[0]))
    print("Primeiros 10 valores:", vectors[0][:10])

# 7. Testar uma consulta
query = "Qual é o assunto principal do documento?"

query_vector = embedding_service.encode_query(query)

print("\nDimensões do vetor da pergunta:", len(query_vector))
