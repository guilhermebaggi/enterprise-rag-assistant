from app.services.retriever import Retriever


# 1. Inicializar o Retriever
retriever = Retriever(top_k=5)


# 2. Criar uma pergunta relacionada ao PDF
query = "Qual é o assunto principal do documento?"


# 3. Recuperar os fragmentos relevantes
results = retriever.retrieve(query)


# 4. Exibir os resultados
print("\n========== RESULTADOS DA RECUPERAÇÃO ==========")

print("Pergunta:", query)
print("Total de resultados:", len(results))

for index, result in enumerate(results, start=1):

    print(f"\nResultado {index}")
    print("Similaridade:", round(result["score"], 4))
    print("Documento:", result["source"])
    print("Página:", result["page"])
    print("Chunk:", result["chunk"])
    print("Conteúdo:")
    print(result["text"][:500])
    print("-" * 60)
