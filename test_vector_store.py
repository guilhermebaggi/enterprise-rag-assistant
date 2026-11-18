from app.services.document_loader import extract_text_from_pdf
from app.services.chunking import create_document_chunks
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


# 1. Extrair o texto do PDF
pdf_path = "documents/documento_teste.pdf"

pages = extract_text_from_pdf(pdf_path)

print("Páginas extraídas:", len(pages))


# 2. Criar os chunks
chunks = create_document_chunks(
    pages,
    chunk_size=1000,
    overlap=200
)

# Adicionar a origem do documento
for chunk in chunks:
    chunk["source"] = pdf_path

print("Chunks gerados:", len(chunks))


# 3. Gerar embeddings
embedding_service = EmbeddingService()

texts = [chunk["text"] for chunk in chunks]

embeddings = embedding_service.encode_documents(texts)

print("Embeddings gerados:", len(embeddings))


# 4. Conectar ao Qdrant
vector_store = VectorStore()

# Criar collection
vector_store.create_collection()


# 5. Armazenar os chunks e embeddings
vector_store.insert_chunks(
    chunks=chunks,
    embeddings=embeddings
)


# 6. Criar uma pergunta
query = "Qual é o assunto principal do documento?"

query_vector = embedding_service.encode_query(query)


# 7. Pesquisar no Qdrant
results = vector_store.search(
    query_vector=query_vector,
    limit=5
)


# 8. Exibir resultados
print("\n========== RESULTADOS DA BUSCA ==========")

for index, result in enumerate(results, start=1):

    print(f"\nResultado {index}")
    print("Similaridade:", round(result["score"], 4))
    print("Página:", result["page"])
    print("Chunk:", result["chunk"])
    print("Texto:", result["text"][:300])
