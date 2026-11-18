from app.services.retriever import Retriever
from app.services.llm import LLMService


# Pergunta que será enviada ao RAG
query = "Qual é o assunto principal do documento?"


# Recupera os trechos relevantes
retriever = Retriever(top_k=5)
retrieved_chunks = retriever.retrieve(query)


# Gera a resposta utilizando o LLM
llm = LLMService()
answer = llm.generate_answer(query, retrieved_chunks)


print("\n========== RESPOSTA DO RAG ==========")
print("Pergunta:", query)
print("\nResposta:")
print(answer)
