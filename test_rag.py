from app.services.rag import RAGService


rag = RAGService(top_k=5)

query = "Quais são as taxas cobradas no condomínio?"

result = rag.ask(query)

print("\n========== RESULTADO DO RAG ==========")

print("\nPergunta:")
print(result["question"])

print("\nResposta:")
print(result["answer"])


print("\nFontes utilizadas:")

for source in result["sources"]:
    print(f"\nDocumento: {source['document']}")
    print(f"Página: {source['page']}")

    for chunk in source["chunks"]:
        print(f"  Chunk: {chunk['chunk']}")
        print(f"  Similaridade: {chunk['score']:.4f}")
