
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Pergunta feita pelo usuário"
    )


class SourceResponse(BaseModel):
    document: str
    page: int
    chunks: list[dict]


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]


class UploadResponse(BaseModel):
    filename: str
    pages_processed: int
    chunks_created: int
    message: str
