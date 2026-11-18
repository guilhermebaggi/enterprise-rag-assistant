from sentence_transformers import SentenceTransformer
import torch

class EmbeddingService:

    def __init__(
        self,
        model_name: str = "intfloat/multilingual-e5-small"
    ):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Carregando modelo na plataforma: {self.device}")

        self.model = SentenceTransformer(
            model_name,
            device=self.device
        )

        print("Modelo de embeddings carregado!")

    def encode_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Converte documentos em vetores numéricos.
        """

        if not texts:
            return []

        prepared_texts = [
            f"passage: {text}" for text in texts
        ]

        embeddings = self.model.encode(
            prepared_texts,
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    def encode_query(self, query: str) -> list[float]:
        """
        Converte uma pergunta em um vetor numérico.
        """

        prepared_query = f"query: {query}"

        embedding = self.model.encode(
            prepared_query,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()
