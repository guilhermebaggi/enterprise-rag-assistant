from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


class Retriever:

    def __init__(self, top_k: int = 5):

        self.top_k = top_k

        # Serviço responsável pelos embeddings
        self.embedding_service = EmbeddingService()

        # Serviço responsável pela busca no Qdrant
        self.vector_store = VectorStore()

    def retrieve(self, query: str) -> list[dict]:
        """
        Recupera os chunks mais relevantes para uma pergunta.
        """

        if not query or not query.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        # 1. Gerar embedding da pergunta
        query_vector = self.embedding_service.encode_query(query)

        # 2. Pesquisar no Qdrant
        results = self.vector_store.search(
            query_vector=query_vector,
            limit=self.top_k
        )

        return results
