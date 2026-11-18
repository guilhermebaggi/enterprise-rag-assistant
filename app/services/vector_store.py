from uuid import uuid5, NAMESPACE_URL

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


class VectorStore:

    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection_name: str = "documents",
        vector_size: int = 384
    ):

        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def create_collection(self):
        """
        Cria a collection caso ela ainda não exista.
        """

        if not self.client.collection_exists(
            collection_name=self.collection_name
        ):

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

            print(f"Collection '{self.collection_name}' criada!")

        else:
            print(f"Collection '{self.collection_name}' já existe.")

    def insert_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]]
    ):
        """
        Armazena os chunks e seus respectivos embeddings.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "A quantidade de chunks e embeddings é diferente."
            )

        if not chunks:
            print("Nenhum chunk para armazenar.")
            return

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            if len(embedding) != self.vector_size:
                raise ValueError(
                    f"Embedding possui {len(embedding)} dimensões. "
                    f"Esperado: {self.vector_size}."
                )

            point = PointStruct(
                id=str(uuid5(
                    NAMESPACE_URL,
                    f"{chunk.get('source', 'unknown')}:{chunk['page']}:{chunk['chunk']}"
                )),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "page": chunk["page"],
                    "chunk": chunk["chunk"],
                    "source": chunk.get("source", "unknown")
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True
        )

        print(f"{len(points)} chunks armazenados no Qdrant!")

    def search(
        self,
        query_vector: list[float],
        limit: int = 5
    ) -> list[dict]:
        """
        Recupera os chunks mais semelhantes à consulta.
        """

        if len(query_vector) != self.vector_size:
            raise ValueError(
                f"Consulta possui {len(query_vector)} dimensões. "
                f"Esperado: {self.vector_size}."
            )

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        )

        results = []

        for point in response.points:

            results.append({
                "id": point.id,
                "score": point.score,
                "text": point.payload.get("text"),
                "page": point.payload.get("page"),
                "chunk": point.payload.get("chunk"),
                "source": point.payload.get("source")
            })

        return results
