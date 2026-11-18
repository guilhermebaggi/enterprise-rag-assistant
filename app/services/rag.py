from app.services.retriever import Retriever
from app.services.llm import LLMService


class RAGService:
    def __init__(self, top_k: int = 5):
        self.retriever = Retriever(top_k=top_k)
        self.llm = LLMService()

    def ask(self, query: str) -> dict:
        if not query or not query.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        # 1. Recuperar os trechos relevantes
        retrieved_chunks = self.retriever.retrieve(query)

        # 2. Gerar a resposta
        answer = self.llm.generate_answer(
            query=query,
            retrieved_chunks=retrieved_chunks
        )

        # 3. Agrupar fontes por documento e página
        grouped_sources = {}

        for chunk in retrieved_chunks:
            key = (chunk["source"], chunk["page"])

            if key not in grouped_sources:
                grouped_sources[key] = {
                    "document": chunk["source"],
                    "page": chunk["page"],
                    "chunks": []
                }

            grouped_sources[key]["chunks"].append({
                "chunk": chunk["chunk"],
                "score": chunk["score"],
                "text": chunk["text"]
            })

        return {
            "question": query,
            "answer": answer,
            "sources": list(grouped_sources.values())
        }
